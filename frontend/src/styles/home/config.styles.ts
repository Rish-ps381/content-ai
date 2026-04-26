export const configStyles = {
  wrap: "border-t border-border p-3",
  planBtn:
    "mb-2 flex w-full items-center gap-3 rounded-lg border border-border bg-card px-3 py-2 text-left text-sm transition-colors hover:bg-accent",
  planIcon: "h-4 w-4 text-primary",
  planRow: "flex flex-1 items-center justify-between",
  planLabel: "font-medium text-foreground",
  planBadge:
    "rounded-full bg-accent px-2 py-0.5 text-[11px] font-semibold uppercase text-accent-foreground",
  settingsBtn:
    "mb-2 flex w-full items-center gap-3 rounded-lg px-3 py-2 text-left text-sm text-foreground/80 transition-colors hover:bg-accent",
  settingsIcon: "h-4 w-4 text-muted-foreground",
  bottomRow: "flex items-center justify-between gap-2",
  profileBtn: "flex items-center gap-2 rounded-lg p-1 transition-colors hover:bg-accent",
  profileAvatar:
    "flex h-9 w-9 items-center justify-center rounded-full text-sm font-semibold text-primary-foreground",
  logoutBtn:
    "flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-foreground/70 transition-colors hover:bg-destructive/10 hover:text-destructive",
  logoutIcon: "h-4 w-4",
} as const;
