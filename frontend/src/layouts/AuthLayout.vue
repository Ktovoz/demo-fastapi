<template>
  <div class="auth-layout">
    <div class="auth-shell">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
// Auth layout wrapper with ambient background
</script>

<style scoped>
.auth-layout {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: clamp(32px, 6vw, 64px);
  background: radial-gradient(circle at 15% 20%, rgba(37, 99, 235, 0.25), transparent 55%),
    radial-gradient(circle at 85% 15%, rgba(236, 72, 153, 0.18), transparent 60%),
    radial-gradient(circle at 50% 85%, rgba(45, 212, 191, 0.2), transparent 55%),
    linear-gradient(140deg, #0f172a 0%, #1e293b 45%, #111827 100%);
  overflow: hidden;
}

.auth-layout::before,
.auth-layout::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.35;
  pointer-events: none;
}

.auth-layout::before {
  width: 420px;
  height: 420px;
  background: rgba(37, 99, 235, 0.55);
  top: clamp(-220px, -10vw, -140px);
  left: clamp(-140px, -8vw, -80px);
}

.auth-layout::after {
  width: 360px;
  height: 360px;
  background: rgba(236, 72, 153, 0.45);
  bottom: clamp(-180px, -8vw, -60px);
  right: clamp(-160px, -10vw, -70px);
}

.auth-shell {
  position: relative;
  width: 100%;
  max-width: 1080px;
}
</style>
