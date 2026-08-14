import { Sparkles } from "lucide-react";
import { appTitleStyles as s } from "@/styles/home/appTitle.styles";

export function AppTitle() {
  return (
    <div className={s.wrap}>
      <div className={s.badge} style={{ background: "var(--gradient-primary)" }}>
        <Sparkles className={s.badgeIcon} />
      </div>
      <div className={s.textBlock}>
        <h1 className={s.title}>Smart Content AI</h1>
        <p className={s.subtitle}>by Stella Apps</p>
      </div>
    </div>
  );
}
