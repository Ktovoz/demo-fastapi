<template>
  <div class="app-shell" :class="shellClasses">
    <aside v-if="!hideSidebar" class="app-shell__sidebar" :class="{ 'app-shell__sidebar--collapsed': sidebarCollapsed }">
      <slot name="sidebar" />
    </aside>

    <div class="app-shell__main">
      <header v-if="!hideHeader" class="app-shell__header">
        <slot name="header" />
      </header>

      <main class="app-shell__content">
        <slot />
      </main>

      <footer v-if="!hideFooter" class="app-shell__footer">
        <slot name="footer" />
      </footer>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  theme: {
    type: String,
    default: 'light'
  },
  sidebarCollapsed: {
    type: Boolean,
    default: false
  },
  hideSidebar: {
    type: Boolean,
    default: false
  },
  hideHeader: {
    type: Boolean,
    default: false
  },
  hideFooter: {
    type: Boolean,
    default: false
  }
})

const shellClasses = computed(() => ({
  [`theme-${props.theme}`]: true,
  'app-shell--no-sidebar': props.hideSidebar
}))
</script>

<style scoped>
:global(:root) {
  --brand-primary: #2563eb;
  --brand-secondary: #0ea5e9;
  --brand-accent: #9333ea;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --surface-background: #f4f7fb;
  --surface-muted: #eef2ff;
  --surface-card: rgba(255, 255, 255, 0.92);
  --surface-elevated: rgba(255, 255, 255, 0.88);
  --border-soft: rgba(15, 23, 42, 0.08);
  --border-strong: rgba(15, 23, 42, 0.12);
  --shadow-soft: 0 12px 32px rgba(15, 23, 42, 0.08);
  --shadow-medium: 0 18px 42px rgba(15, 23, 42, 0.12);
  --app-sidebar-width: 256px;
  --app-sidebar-width-collapsed: 84px;
  --header-height: 82px;
}

:global(body) {
  margin: 0;
  background: linear-gradient(180deg, var(--surface-background) 0%, #ffffff 65%, var(--surface-background) 100%);
  font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: var(--text-primary);
}

.app-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: auto 1fr;
  background: transparent;
}

.app-shell__sidebar {
  position: relative;
  z-index: 2;
  width: var(--app-sidebar-width);
  transition: width 0.25s ease;
}

.app-shell__sidebar--collapsed {
  width: var(--app-sidebar-width-collapsed);
}

.app-shell__main {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  background: transparent;
}

.app-shell__header {
  position: sticky;
  top: 0;
  z-index: 20;
}

.app-shell__content {
  position: relative;
  z-index: 1;
  min-height: 100%;
  padding: calc(var(--header-height) * 0.65) clamp(20px, 4vw, 36px) clamp(40px, 6vw, 72px);
  box-sizing: border-box;
}

.app-shell__footer {
  position: relative;
  z-index: 10;
  padding: 16px 32px;
  color: var(--text-secondary);
}

.app-shell--no-sidebar {
  grid-template-columns: 1fr;
}

@media (max-width: 1200px) {
  :global(:root) {
    --app-sidebar-width: 232px;
  }
}

@media (max-width: 992px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .app-shell__sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    transform: translateX(-100%);
  }
}
</style>
