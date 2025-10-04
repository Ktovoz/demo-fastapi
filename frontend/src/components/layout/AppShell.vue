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
.app-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: auto 1fr;
  background: var(--app-shell-bg, linear-gradient(140deg, #eef2ff 0%, #f8fafc 45%, #e2e8f0 100%));
}

.app-shell::before,
.app-shell::after {
  content: '';
  position: fixed;
  border-radius: 50%;
  filter: blur(140px);
  opacity: 0.3;
  pointer-events: none;
}

.app-shell::before {
  width: 420px;
  height: 420px;
  top: -160px;
  left: -140px;
  background: rgba(59, 130, 246, 0.35);
}

.app-shell::after {
  width: 360px;
  height: 360px;
  right: -140px;
  bottom: -160px;
  background: rgba(236, 72, 153, 0.28);
}

.app-shell__sidebar {
  position: relative;
  z-index: 2;
  width: var(--app-sidebar-width, 240px);
  transition: width 0.2s ease;
  background: transparent;
}

.app-shell__sidebar--collapsed {
  width: var(--app-sidebar-width-collapsed, 88px);
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
}

.app-shell__footer {
  position: relative;
  z-index: 10;
}

.app-shell--no-sidebar {
  grid-template-columns: 1fr;
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
