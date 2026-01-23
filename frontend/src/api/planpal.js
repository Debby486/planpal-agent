const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function planDay(prompt) {
  const res = await fetch(BASE_URL + "/api/agent/plan-day/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: prompt }),
  });

  const data = await res.json();

  if (!res.ok) {
    const message = data && data.error ? data.error : "Request failed";
    throw new Error(message);
  }

  return data;
}
