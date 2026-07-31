// Calorie Tracker front-end. Vanilla JS, no build step, no framework.

const state = {
  date: todayISO(),
  selectedFood: null,
  searchTimer: null,
};

const RING_CIRCUMFERENCE = 2 * Math.PI * 78; // matches r=78 in the SVG
const MEAL_ICONS = { breakfast: "🌅", lunch: "☀️", dinner: "🌙", snack: "🍎" };

function todayISO() {
  const d = new Date();
  const offset = d.getTimezoneOffset();
  const local = new Date(d.getTime() - offset * 60 * 1000);
  return local.toISOString().slice(0, 10);
}

function shiftDate(iso, days) {
  const d = new Date(iso + "T00:00:00");
  d.setDate(d.getDate() + days);
  return d.toISOString().slice(0, 10);
}

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const body = await res.json().catch(() => null);
  if (!res.ok) {
    throw new Error((body && body.error) || `Request failed (${res.status})`);
  }
  return body;
}

// ---------------------------------------------------------------- init ---
document.addEventListener("DOMContentLoaded", () => {
  const dateInput = document.getElementById("logDate");
  dateInput.value = state.date;

  dateInput.addEventListener("change", () => {
    state.date = dateInput.value;
    refreshDateViews();
  });
  document.getElementById("prevDay").addEventListener("click", () => {
    state.date = shiftDate(state.date, -1);
    dateInput.value = state.date;
    refreshDateViews();
  });
  document.getElementById("nextDay").addEventListener("click", () => {
    state.date = shiftDate(state.date, 1);
    dateInput.value = state.date;
    refreshDateViews();
  });

  document.getElementById("foodSearch").addEventListener("input", onSearchInput);
  document.getElementById("addLogBtn").addEventListener("click", onAddLogEntry);
  document.getElementById("saveCustomFoodBtn").addEventListener("click", onSaveCustomFood);
  document.getElementById("profileForm").addEventListener("submit", onSaveProfile);

  loadProfile();
  refreshDateViews();
});

function refreshDateViews() {
  loadLog();
  loadSummary();
}

// -------------------------------------------------------------- search ---
function onSearchInput(e) {
  const q = e.target.value.trim();
  clearTimeout(state.searchTimer);
  if (!q) {
    document.getElementById("searchResults").innerHTML = "";
    return;
  }
  state.searchTimer = setTimeout(() => runSearch(q), 200);
}

async function runSearch(q) {
  const results = await api(`/api/foods?q=${encodeURIComponent(q)}`);
  const container = document.getElementById("searchResults");
  container.innerHTML = "";
  results.forEach((food) => {
    const item = document.createElement("div");
    item.className = "search-result-item";
    item.innerHTML = `
      <span>${escapeHtml(food.name)}</span>
      <span class="sr-meta">${escapeHtml(food.serving_desc)} &middot; ${Math.round(food.calories)} cal</span>
    `;
    item.addEventListener("click", () => selectFood(food));
    container.appendChild(item);
  });
  if (results.length === 0) {
    container.innerHTML = `<div class="search-result-item"><span class="sr-meta">No matches. Try "Add a custom food" below.</span></div>`;
  }
}

function selectFood(food) {
  state.selectedFood = food;
  document.getElementById("searchResults").innerHTML = "";
  document.getElementById("foodSearch").value = food.name;
  document.getElementById("selectedFoodRow").hidden = false;
  document.getElementById("selectedFoodName").textContent = food.name;
  document.getElementById("selectedServingDesc").textContent = `per ${food.serving_desc}`;
  document.getElementById("servingsInput").value = 1;
}

async function onAddLogEntry() {
  if (!state.selectedFood) return;
  const servings = parseFloat(document.getElementById("servingsInput").value) || 1;
  const meal = document.getElementById("mealSelect").value;

  await api("/api/log", {
    method: "POST",
    body: JSON.stringify({
      date: state.date,
      meal,
      food_id: state.selectedFood.id,
      servings,
    }),
  });

  state.selectedFood = null;
  document.getElementById("selectedFoodRow").hidden = true;
  document.getElementById("foodSearch").value = "";
  refreshDateViews();
}

async function onSaveCustomFood() {
  const name = document.getElementById("customName").value.trim();
  if (!name) {
    alert("Give the food a name first.");
    return;
  }
  const payload = {
    name,
    serving_desc: document.getElementById("customServing").value.trim() || "1 serving",
    calories: document.getElementById("customCalories").value || 0,
    protein_g: document.getElementById("customProtein").value || 0,
    carbs_g: document.getElementById("customCarbs").value || 0,
    fat_g: document.getElementById("customFat").value || 0,
  };
  const food = await api("/api/foods", { method: "POST", body: JSON.stringify(payload) });

  ["customName", "customServing", "customCalories", "customProtein", "customCarbs", "customFat"].forEach(
    (id) => (document.getElementById(id).value = "")
  );

  selectFood(food);
}

// ----------------------------------------------------------------- log ---
async function loadLog() {
  const entries = await api(`/api/log?date=${state.date}`);
  const container = document.getElementById("logList");
  container.innerHTML = "";

  if (entries.length === 0) {
    container.innerHTML = `<p class="empty-state">No food logged yet for this day.</p>`;
    return;
  }

  const meals = ["breakfast", "lunch", "dinner", "snack"];
  meals.forEach((meal) => {
    const mealEntries = entries.filter((e) => e.meal === meal);
    if (mealEntries.length === 0) return;

    const title = document.createElement("div");
    title.className = "meal-group-title";
    title.textContent = `${MEAL_ICONS[meal] || ""} ${meal}`;
    container.appendChild(title);

    mealEntries.forEach((entry) => {
      const row = document.createElement("div");
      row.className = "log-entry";
      row.innerHTML = `
        <div class="log-entry-info">
          <span>${escapeHtml(entry.food_name)}</span>
          <span class="log-entry-servings">${entry.servings} serving(s)</span>
        </div>
        <div class="log-entry-right">
          <span class="log-entry-cals">${Math.round(entry.calories)} cal</span>
          <button class="delete-btn" title="Remove">&times;</button>
        </div>
      `;
      row.querySelector(".delete-btn").addEventListener("click", async () => {
        await api(`/api/log/${entry.id}`, { method: "DELETE" });
        refreshDateViews();
      });
      container.appendChild(row);
    });
  });
}

async function loadSummary() {
  const summary = await api(`/api/summary?date=${state.date}`);

  document.getElementById("sumCalories").textContent = Math.round(summary.calories);
  document.getElementById("sumGoal").textContent =
    summary.calorie_goal != null ? Math.round(summary.calorie_goal) : "—";

  const remainingEl = document.getElementById("sumRemaining");
  const remainingStat = document.getElementById("remainingStat");
  if (summary.remaining != null) {
    const remaining = Math.round(summary.remaining);
    remainingEl.textContent = remaining;
    remainingStat.classList.toggle("over", remaining < 0);
  } else {
    remainingEl.textContent = "—";
    remainingStat.classList.remove("over");
  }

  const macroCalorieBasis = Math.max(summary.calories, 1);
  setMacroBar("Protein", summary.protein_g, (summary.protein_g * 4) / macroCalorieBasis);
  setMacroBar("Carbs", summary.carbs_g, (summary.carbs_g * 4) / macroCalorieBasis);
  setMacroBar("Fat", summary.fat_g, (summary.fat_g * 9) / macroCalorieBasis);

  setCalorieRing(summary.calories, summary.calorie_goal);
}

function setCalorieRing(calories, goal) {
  const ring = document.getElementById("ringFill");
  const fraction = goal ? Math.min(1, calories / goal) : 0;
  const offset = RING_CIRCUMFERENCE * (1 - fraction);
  ring.style.strokeDasharray = `${RING_CIRCUMFERENCE}`;
  ring.style.strokeDashoffset = `${offset}`;
}

function setMacroBar(label, grams, fraction) {
  const bar = document.getElementById(`bar${label}`);
  const val = document.getElementById(`val${label}`);
  bar.style.width = `${Math.min(100, Math.round(fraction * 100))}%`;
  val.textContent = `${Math.round(grams)}g`;
}

// ------------------------------------------------------------- profile ---
async function loadProfile() {
  const profile = await api("/api/profile");
  if (!profile) return;

  document.getElementById("pSex").value = profile.sex;
  document.getElementById("pAge").value = profile.age;
  document.getElementById("pHeight").value = profile.height_cm;
  document.getElementById("pWeight").value = profile.weight_kg;
  document.getElementById("pActivity").value = profile.activity_level;
  document.getElementById("pGoal").value = profile.goal;

  showProfileResult(profile);
}

async function onSaveProfile(e) {
  e.preventDefault();
  const payload = {
    sex: document.getElementById("pSex").value,
    age: document.getElementById("pAge").value,
    height_cm: document.getElementById("pHeight").value,
    weight_kg: document.getElementById("pWeight").value,
    activity_level: document.getElementById("pActivity").value,
    goal: document.getElementById("pGoal").value,
  };

  try {
    const profile = await api("/api/profile", { method: "POST", body: JSON.stringify(payload) });
    showProfileResult(profile);
    loadSummary();
  } catch (err) {
    alert(err.message);
  }
}

function showProfileResult(profile) {
  document.getElementById("profileResult").hidden = false;
  document.getElementById("rBmr").textContent = Math.round(profile.bmr);
  document.getElementById("rTdee").textContent = Math.round(profile.tdee);
  document.getElementById("rGoal").textContent = Math.round(profile.calorie_goal);
}

// --------------------------------------------------------------- utils ---
function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
