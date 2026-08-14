import { Settings, LogOut, Crown } from "lucide-react";
import { configStyles as s } from "@/styles/home/config.styles";

interface ConfigProps {
  plan?: string;
  firstName?: string;
}

export function Config({ plan = "Free", firstName = "U" }: ConfigProps) {
  const initial = firstName.charAt(0).toUpperCase();
  return (
    <div className={s.wrap}>
      <button type="button" className={s.planBtn}>
        <Crown className={s.planIcon} />
        <div className={s.planRow}>
          <span className={s.planLabel}>Plan</span>
          <span className={s.planBadge}>{plan}</span>
        </div>
      </button>

      <button type="button" className={s.settingsBtn}>
        <Settings className={s.settingsIcon} />
        <span>Settings</span>
      </button>

      <div className={s.bottomRow}>
        <button type="button" className={s.profileBtn} aria-label="Profile">
          <span
            className={s.profileAvatar}
            style={{ background: "var(--gradient-primary)" }}
          >
            {initial}
          </span>
        </button>
        <button type="button" className={s.logoutBtn}>
          <LogOut className={s.logoutIcon} />
          Logout
        </button>
      </div>
    </div>
  );
}
