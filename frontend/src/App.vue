<template>
  <div class="page" :class="{ 'page--center': !result }">
    <div class="shell">
      <header class="header">
        <h1 class="title" aria-label="PlanPal">
          <span
            v-for="(ch, i) in titleLetters"
            :key="i"
            class="titleLetter"
            :style="{ animationDelay: (i * 70) + 'ms' }"
          >
            {{ ch }}
          </span>
        </h1>

        <p class="subtitle">Hello! I’m an agentic AI</p>
        <p class="desc">I’ll take the stress off you, plan your day and send reminders to your mailbox.</p>
      </header>

      <section class="card">
        <label class="label">How do you want your day to go?</label>

        <textarea
          v-model="prompt"
          class="textarea"
          placeholder="e.g. Plan my day tomorrow: deep work, groceries, gym. Remind me 1 minute before each."
          rows="4"
        />

        <div class="row">
          <button class="btn" :disabled="loading || !prompt.trim()" @click="generatePlan">
            <span v-if="loading">Planning…</span>
            <span v-else>Generate Plan</span>
          </button>

          <button class="btn reset" :disabled="loading" @click="onReset">
            Reset
          </button>
        </div>

        <p v-if="error" class="error">{{ error }}</p>
      </section>

      <!-- Results -->
      <section v-if="result" class="results">
        <p class="intro">
          Here are your plans for tomorrow:
        </p>

        <div class="grid">
          <div class="card">
            <div class="cardHeader">
              <h2>Your plan</h2>
              <span class="pill">
                Date: <b>{{ result.plan.date }}</b>
              </span>
            </div>

            <ul class="list">
              <li v-for="(t, idx) in result.plan.tasks" :key="idx" class="item">
                <div class="itemTop">
                  <div class="itemTitle">{{ t.title }}</div>
                  <span class="tag" :style="{ background: t.color || 'rgba(148, 163, 184, 0.18)' }">
                    {{ t.category || "Other" }}
                  </span>
                </div>

                <div class="itemMeta">Due: {{ formatDateTime(t.due_at) }}</div>
                <div class="itemMeta">Reminder: {{ t.remind_minutes_before }} min before</div>
              </li>
            </ul>

            <p class="note">
              Reminders will be sent to your email before each task.
            </p>
          </div>
        </div>
      </section>

      <footer class="footer">
        <span class="muted">Have a productive day ahead!</span>
      </footer>
    </div>
  </div>
</template>


<script>
import { planDay } from "./api/planpal";

export default {
  data() {
    return {
      prompt: "Plan my day tomorrow: deep work, groceries, gym. Remind me 1 minute before each.",
      loading: false,
      error: "",
      result: null,
      titleLetters: "PlanPal".split(""),
    };
  },
  methods: {
    async generatePlan() {
      this.error = "";
      this.result = null;
      this.loading = true;

      try {
        const data = await planDay(this.prompt);
        this.result = data;
      } catch (e) {
        this.error = e && e.message ? e.message : "Something went wrong";
      } finally {
        this.loading = false;
      }
    },

    onReset() {
      this.prompt = "";
      this.error = "";
      this.result = null;
    },

    formatDateTime(value) {
      if (!value) return "-";
      const d = new Date(value);
      if (Number.isNaN(d.getTime())) return value;
      return d.toLocaleString();
    },
  },
};
</script>



<style>
.page {
  max-width: 980px;
  margin: 0 auto;
  padding: 52px 16px 60px;
  min-height: 100vh;

  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
  color: rgba(0, 0, 0, 0.86);

  background:
    radial-gradient(900px 400px at 50% -60px, rgba(99, 102, 241, 0.12), transparent 60%),
    radial-gradient(900px 500px at 10% 10%, rgba(244, 63, 94, 0.08), transparent 55%),
    radial-gradient(900px 500px at 90% 20%, rgba(16, 185, 129, 0.07), transparent 55%);
}

.page--center {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: clamp(40px, 10vh, 120px);
  padding-bottom: 40px;
}

.shell {
  width: 100%;
}

.header {
  text-align: center;
  margin-bottom: 18px;
}

.title {
  margin: 0;
  font-size: 46px;
  letter-spacing: -0.03em;
  line-height: 1.05;
}

.titleLetter {
  display: inline-block;
  animation: hop 900ms ease-in-out infinite;
}

@keyframes hop {
  0%,
  80%,
  100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-8px);
  }
}

.subtitle {
  margin: 10px 0 0;
  font-size: 16px;
  font-weight: 600;
  opacity: 0.78;
}

.desc {
  margin: 6px 0 0;
  opacity: 0.72;
}


.card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 18px;
  padding: 18px;
  backdrop-filter: blur(6px);
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.06), 0 2px 10px rgba(0, 0, 0, 0.03);
}

.label {
  display: block;
  margin-bottom: 10px;
  text-align: center;
  font-weight: 800;
}

.textarea {
  width: 100%;
  padding: 12px 14px;
  box-sizing: border-box;

  border: 1px solid rgba(0, 0, 0, 0.14);
  border-radius: 14px;
  background: #fff;

  resize: vertical;
  outline: none;
  font-size: 15px;
  line-height: 1.45;
}

.textarea:focus {
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

/* Buttons row */
.row {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
}

.btn {
  padding: 10px 14px;
  border-radius: 14px;
  border: 1px solid rgba(0, 0, 0, 0.12);

  cursor: pointer;
  font-weight: 800;
  color: #fff;
  background: rgba(17, 24, 39, 0.95);

  transition: transform 120ms ease, opacity 120ms ease, box-shadow 120ms ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.1);
}

.btn:active {
  transform: translateY(0);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.reset {
  background: rgba(255, 255, 255, 0.65);
  color: rgba(0, 0, 0, 0.86);
}

.error {
  margin-top: 12px;
  text-align: center;
  font-weight: 700;
  color: #b42318;
}


.results {
  margin-top: 14px;
}

.intro {
  margin: 10px 0 14px;
  text-align: center;
  font-weight: 800;
  opacity: 0.82;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
  margin-top: 14px;
}

.cardHeader {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 6px;
}

.card h2 {
  margin: 0;
  font-size: 18px;
  letter-spacing: -0.01em;
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;

  border-radius: 999px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.7);

  font-size: 13px;
  opacity: 0.85;
}

.list {
  list-style: none;
  padding: 0;
  margin: 12px 0 0;
  display: grid;
  gap: 10px;
}

.item {
  padding: 12px 14px;

  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.95);
}

.itemTop {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.itemTitle {
  font-weight: 900;
  letter-spacing: -0.01em;
}

.tag {
  display: inline-flex;
  align-items: center;
  padding: 6px 10px;

  border-radius: 999px;
  border: 1px solid rgba(0, 0, 0, 0.08);

  font-size: 12.5px;
  font-weight: 800;
  white-space: nowrap;
}

.itemMeta {
  margin-top: 6px;
  font-size: 13.5px;
  line-height: 1.35;
  opacity: 0.75;
}

.note {
  margin-top: 14px;
  text-align: center;
  font-weight: 700;
  opacity: 0.75;
}


.footer {
  margin-top: 18px;
  text-align: center;
  font-size: 14px;
  opacity: 0.78;
}

.muted {
  opacity: 0.75;
}
</style>
