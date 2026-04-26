import { Twitter, Linkedin, Instagram, Megaphone } from "lucide-react";
import { quickTypeStyles as s } from "@/styles/home/quickType.styles";

const QUICK_TYPES = [
  { label: "Tweets / X posts", icon: Twitter },
  { label: "LinkedIn posts", icon: Linkedin },
  { label: "Instagram captions", icon: Instagram },
  { label: "Hooks / headlines", icon: Megaphone },
];

export function QuickType() {
  return (
    <div className={s.wrap}>
      <p className={s.label}>Quick Type</p>
      <ul className={s.list}>
        {QUICK_TYPES.map(({ label, icon: Icon }) => (
          <li key={label}>
            <button type="button" className={s.button}>
              <Icon className={s.icon} />
              <span className={s.text}>{label}</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
