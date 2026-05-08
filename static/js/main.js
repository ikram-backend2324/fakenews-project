/* FakeNews AI — Main JS */

document.addEventListener('DOMContentLoaded', function () {

  // ─── Auto-dismiss alerts ───────────────────────────────
  document.querySelectorAll('.alert-auto-dismiss').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.4s ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });

  // ─── Animate stats on scroll ──────────────────────────
  const counters = document.querySelectorAll('.count-up');
  const observerOpts = { threshold: 0.5 };

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.getAttribute('data-target') || el.textContent, 10);
        animateCount(el, target);
        counterObserver.unobserve(el);
      }
    });
  }, observerOpts);

  counters.forEach(c => counterObserver.observe(c));

  function animateCount(el, target) {
    let start = 0;
    const duration = 1200;
    const step = Math.ceil(target / (duration / 16));
    const timer = setInterval(() => {
      start = Math.min(start + step, target);
      el.textContent = start;
      if (start >= target) clearInterval(timer);
    }, 16);
  }

  // ─── Scroll reveal ────────────────────────────────────
  const revealEls = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  revealEls.forEach(el => revealObserver.observe(el));

  // ─── Typing effect on hero ────────────────────────────
  const typeTarget = document.getElementById('typing-text');
  if (typeTarget) {
    const phrases = typeTarget.getAttribute('data-phrases').split('|');
    let pi = 0, ci = 0, deleting = false;

    function type() {
      const phrase = phrases[pi];
      if (!deleting) {
        typeTarget.textContent = phrase.substring(0, ci + 1);
        ci++;
        if (ci === phrase.length) {
          deleting = true;
          setTimeout(type, 2000);
          return;
        }
      } else {
        typeTarget.textContent = phrase.substring(0, ci - 1);
        ci--;
        if (ci === 0) {
          deleting = false;
          pi = (pi + 1) % phrases.length;
        }
      }
      setTimeout(type, deleting ? 50 : 90);
    }
    setTimeout(type, 800);
  }

  // ─── Character counter ────────────────────────────────
  const textarea = document.getElementById('newsText');
  const counter = document.getElementById('charCounter');

  if (textarea && counter) {
    const max = 5000;
    textarea.addEventListener('input', () => {
      const len = textarea.value.length;
      counter.textContent = `${len} / ${max}`;
      counter.classList.remove('warn', 'over');
      if (len > max * 0.85) counter.classList.add('warn');
      if (len > max) counter.classList.add('over');
    });
  }
});

// ─── Loading Overlay ────────────────────────────────────
const loadingMessages = [
  null,  // will be filled from data-* attrs
];

function showLoading() {
  const overlay = document.getElementById('loadingOverlay');
  if (!overlay) return;
  overlay.classList.add('active');

  const msgs = overlay.getAttribute('data-messages');
  if (msgs) {
    const arr = msgs.split('|');
    const msgEl = overlay.querySelector('.loading-text');
    if (msgEl) {
      let idx = 0;
      msgEl.textContent = arr[0];
      window.__loadingInterval = setInterval(() => {
        idx = (idx + 1) % arr.length;
        msgEl.style.opacity = '0';
        setTimeout(() => {
          msgEl.textContent = arr[idx];
          msgEl.style.opacity = '1';
        }, 200);
      }, 2500);
    }
  }
}

function hideLoading() {
  const overlay = document.getElementById('loadingOverlay');
  if (!overlay) return;
  overlay.classList.remove('active');
  if (window.__loadingInterval) {
    clearInterval(window.__loadingInterval);
    window.__loadingInterval = null;
  }
}

// ─── Analysis Form Submission ───────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  const analyzeForm = document.getElementById('analyzeForm');
  if (!analyzeForm) return;

  analyzeForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    const text = document.getElementById('newsText').value.trim();
    if (text.length < 30) {
      showFormError(analyzeForm, window._t?.minLen || 'Please enter at least 30 characters.');
      return;
    }

    showLoading();
    hideResult();

    const formData = new FormData(analyzeForm);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
      const resp = await fetch(analyzeForm.getAttribute('data-url'), {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        body: formData,
      });

      const data = await resp.json();
      hideLoading();

      if (data.success) {
        showResult(data);
      } else {
        const errMsg = data.errors?.news_text?.[0] || (window._t?.error || 'Something went wrong.');
        showFormError(analyzeForm, errMsg);
      }
    } catch (err) {
      hideLoading();
      showFormError(analyzeForm, window._t?.networkError || 'Network error. Please try again.');
    }
  });
});

function showFormError(form, msg) {
  let errDiv = form.querySelector('.form-error-msg');
  if (!errDiv) {
    errDiv = document.createElement('div');
    errDiv.className = 'alert alert-danger form-error-msg mt-2';
    form.prepend(errDiv);
  }
  errDiv.textContent = msg;
  setTimeout(() => errDiv?.remove(), 5000);
}

function hideResult() {
  const rs = document.getElementById('resultSection');
  if (rs) rs.classList.remove('show');
}

function showResult(data) {
  const rs = document.getElementById('resultSection');
  if (!rs) return;

  const verdictMap = {
    fake:      { label: window._t?.fake      || 'FAKE',      icon: 'fa-times-circle' },
    real:      { label: window._t?.real      || 'REAL',      icon: 'fa-check-circle' },
    uncertain: { label: window._t?.uncertain || 'UNCERTAIN', icon: 'fa-question-circle' },
  };

  const info = verdictMap[data.verdict] || verdictMap.uncertain;

  // Update verdict card classes
  const card = rs.querySelector('.verdict-card');
  card.className = `verdict-card verdict-${data.verdict}`;

  // Icon
  const iconEl = rs.querySelector('.verdict-icon-wrap i');
  if (iconEl) { iconEl.className = `fas ${info.icon}`; }

  // Label
  const labelEl = rs.querySelector('.verdict-label');
  if (labelEl) labelEl.textContent = window._t?.verdict || 'VERDICT';

  // Title
  const titleEl = rs.querySelector('.verdict-title');
  if (titleEl) titleEl.textContent = info.label;

  // Confidence
  const pctEl = rs.querySelector('.confidence-pct');
  if (pctEl) pctEl.textContent = data.confidence + '%';

  const fill = rs.querySelector('.confidence-fill');
  if (fill) {
    fill.style.width = '0';
    setTimeout(() => { fill.style.width = data.confidence + '%'; }, 100);
  }

  // Reasoning
  const reasonEl = rs.querySelector('.reasoning-text');
  if (reasonEl) reasonEl.textContent = data.reasoning;

  // Detail link
  const detailLink = rs.querySelector('.detail-link');
  if (detailLink && data.analysis_id) {
    detailLink.href = detailLink.getAttribute('data-base') + data.analysis_id + '/';
    detailLink.style.display = 'inline-flex';
  }

  rs.classList.add('show');
  rs.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
