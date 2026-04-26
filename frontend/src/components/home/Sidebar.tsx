import { Link } from "@tanstack/react-router";
import { Plus } from "lucide-react";
import { AppTitle } from "./sidebar/AppTitle";
import { QuickType } from "./sidebar/QuickType";
import { Chats } from "./sidebar/Chats";
import { Config } from "./sidebar/Config";
import { sidebarStyles as s } from "@/styles/home/sidebar.styles";

interface SidebarInnerProps {
  /** Called after a navigation item is activated (used to close mobile drawer). */
  onNavigate?: () => void;
}

/** Shared sidebar content — used by both desktop aside and mobile drawer. */
export function SidebarInner({ onNavigate }: SidebarInnerProps) {
  return (
    <>
      <AppTitle />

      <div className={s.createWrap}>
        <Link
          to="/home/create"
          activeProps={{ className: s.createBtnActive }}
          className={s.createBtn}
          style={{ background: "var(--gradient-primary)" }}
          onClick={onNavigate}
        >
          <Plus className={s.icon} />
          Create
        </Link>
      </div>

      <QuickType />
      <Chats />
      <Config />
    </>
  );
}

/** Desktop sidebar — hidden on small screens. */
export function Sidebar() {
  return (
    <aside className={s.aside}>
      <SidebarInner />
    </aside>
  );
}
