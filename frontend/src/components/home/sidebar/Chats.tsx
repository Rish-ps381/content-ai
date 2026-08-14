import { useEffect, useRef, useState, useCallback } from "react";
import { MessageSquare, Loader2 } from "lucide-react";
import { chatsStyles as s } from "@/styles/home/chats.styles";

interface Conversation {
  id: string;
  type: string | null;
  title: string | null;
}

interface ApiResponse {
  success: boolean;
  data?: Conversation[];
  next_cursor?: string | null;
  error?: string;
}

const API_BASE = ""; // same origin; adjust if backend lives elsewhere
const FIRST_PAGE_LIMIT = 8;
const PAGE_LIMIT = 10;

export function refreshChats() {
  window.dispatchEvent(new CustomEvent("chats:refresh"));
}

export function Chats() {
  const [items, setItems] = useState<Conversation[]>([]);
  const [cursor, setCursor] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);
  const sentinelRef = useRef<HTMLDivElement | null>(null);

  const fetchPage = useCallback(
    async (nextCursor: string | null, limit: number, replace = false) => {
      setLoading(true);
      setError(null);
      try {
        const params = new URLSearchParams();
        params.set("limit", String(limit));
        if (nextCursor) params.set("cursor", nextCursor);
        const res = await fetch(`${API_BASE}/chats/get_conversations?${params.toString()}`, {
          credentials: "include",
        });
        const json: ApiResponse = await res.json();
        if (!json.success) throw new Error(json.error || "Failed to load chats");
        const data = json.data ?? [];
        setItems((prev) => (replace ? data : [...prev, ...data]));
        setCursor(json.next_cursor ?? null);
        if (!json.next_cursor || data.length < limit) setHasMore(false);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load chats");
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  useEffect(() => {
    fetchPage(null, FIRST_PAGE_LIMIT, true);
  }, [fetchPage]);

  useEffect(() => {
    const handler = () => {
      setHasMore(true);
      fetchPage(null, FIRST_PAGE_LIMIT, true);
    };
    window.addEventListener("chats:refresh", handler);
    return () => window.removeEventListener("chats:refresh", handler);
  }, [fetchPage]);

  useEffect(() => {
    if (!sentinelRef.current || !scrollRef.current) return;
    const obs = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !loading && cursor) {
          fetchPage(cursor, PAGE_LIMIT);
        }
      },
      { root: scrollRef.current, rootMargin: "80px" },
    );
    obs.observe(sentinelRef.current);
    return () => obs.disconnect();
  }, [cursor, hasMore, loading, fetchPage]);

  return (
    <div className={s.wrap}>
      <p className={s.label}>Chats</p>
      <div ref={scrollRef} className={s.scroll}>
        {items.length === 0 && !loading && !error && (
          <p className={s.empty}>No conversations yet.</p>
        )}
        {error && <p className={s.error}>{error}</p>}
        <ul className={s.list}>
          {items.map((c) => (
            <li key={c.id}>
              <button type="button" className={s.itemBtn}>
                <MessageSquare className={s.itemIcon} />
                <div className={s.itemBody}>
                  <p className={s.itemTitle}>{c.title || "Untitled"}</p>
                  {c.type && <p className={s.itemType}>{c.type}</p>}
                </div>
              </button>
            </li>
          ))}
        </ul>
        <div ref={sentinelRef} className={s.sentinel} />
        {loading && (
          <div className={s.loadingRow}>
            <Loader2 className={s.loadingIcon} />
          </div>
        )}
        {!hasMore && items.length > 0 && <p className={s.endRow}>End of chats</p>}
      </div>
    </div>
  );
}
