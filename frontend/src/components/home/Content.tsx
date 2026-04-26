import { useState } from "react";
import { Sparkles, Wand2, History, Plus } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { contentStyles as s } from "@/styles/home/content.styles";

const TONES = ["Professional", "Casual", "Witty", "Inspirational", "Bold", "Friendly"];
const AUDIENCES = [
  "Busy professionals",
  "Founders & Entrepreneurs",
  "Marketers",
  "Developers",
  "Creators",
  "Students",
];

export function Content() {
  const [form, setForm] = useState({
    title: "",
    tone: "",
    audience: "",
    goal: "",
    keywords: "",
    notes: "",
  });

  const update =
    (key: keyof typeof form) =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
      setForm((f) => ({ ...f, [key]: e.target.value }));

  const handleGenerate = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Generate:", form);
  };

  return (
    <div className={s.page} style={{ background: "var(--gradient-subtle)" }}>
      <div className={s.container}>
        <div className={s.header}>
          <h1 className={s.title} style={{ backgroundImage: "var(--gradient-primary)" }}>
            AI Content Generator
          </h1>
          <p className={s.subtitle}>Create professional content in seconds</p>

          <div className={s.actionsRow}>
            <button type="button" className={s.actionBtn}>
              <History className={s.actionIcon} />
              View History
            </button>
            <button type="button" className={s.actionBtn}>
              <Plus className={s.actionIcon} />
              Manage Sources
            </button>
          </div>
        </div>

        <form onSubmit={handleGenerate} className={s.card}>
          <div className={s.cardHead}>
            <Sparkles className={s.cardHeadIcon} />
            <h2 className={s.cardHeadTitle}>Generate New Content</h2>
          </div>

          <div className={s.grid}>
            <Field label="Title" required className={s.full}>
              <input
                value={form.title}
                onChange={update("title")}
                placeholder="e.g., 10 Tips for Better Sleep"
                className="form-input"
                required
              />
            </Field>

            <Field label="Tone" required>
              <Select value={form.tone} onValueChange={(v) => setForm((f) => ({ ...f, tone: v }))}>
                <SelectTrigger className={s.selectTrigger}>
                  <SelectValue placeholder="Select a tone" />
                </SelectTrigger>
                <SelectContent>
                  {TONES.map((t) => (
                    <SelectItem key={t} value={t}>
                      {t}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Field>

            <Field label="Audience" required>
              <Select
                value={form.audience}
                onValueChange={(v) => setForm((f) => ({ ...f, audience: v }))}
              >
                <SelectTrigger className={s.selectTrigger}>
                  <SelectValue placeholder="Select an audience" />
                </SelectTrigger>
                <SelectContent>
                  {AUDIENCES.map((a) => (
                    <SelectItem key={a} value={a}>
                      {a}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Field>

            <Field label="Goal" required className={s.full}>
              <input
                value={form.goal}
                onChange={update("goal")}
                placeholder="e.g., Drive newsletter signups"
                className="form-input"
                required
              />
            </Field>

            <Field label="Keywords" required className={s.full}>
              <input
                value={form.keywords}
                onChange={update("keywords")}
                placeholder="Enter target keywords (comma separated)"
                className="form-input"
                required
              />
            </Field>

            <Field label="Notes" className={s.full}>
              <textarea
                value={form.notes}
                onChange={update("notes")}
                placeholder="Anything else the AI should know? (optional)"
                rows={4}
                className="form-input resize-none"
              />
            </Field>
          </div>

          <button
            type="submit"
            className={s.generateBtn}
            style={{ background: "var(--gradient-primary)" }}
          >
            <Wand2 className={s.generateIcon} />
            Generate
          </button>
        </form>
      </div>
    </div>
  );
}

function Field({
  label,
  required,
  className,
  children,
}: {
  label: string;
  required?: boolean;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div className={className}>
      <label className={s.fieldLabel}>
        {label} {required && <span className={s.fieldLabelStar}>*</span>}
      </label>
      {children}
    </div>
  );
}
