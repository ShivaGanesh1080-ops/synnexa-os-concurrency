/**
 * AVENORA EVENTS — Global Hackathons & Tech Summits
 * Client Application Logic & Concurrency Engine Interface
 * SR University • CSE Core • Operating Systems Lab • Product #8
 */

;(function () {
  'use strict';

  // Global State
  const state = {
    hackathons: [],
    filteredHackathons: [],
    settings: {
      razorpay_key_id: 'rzp_test_1DP5mmOlF5G5ag',
      currency: 'INR'
    },
    activeCityFilter: 'ALL',
    activeCategoryFilter: 'ALL',
    searchQuery: '',
    selectedEventForBooking: null,
    pollInterval: null
  };

  const page = document.body.getAttribute('data-page') || 'hub';

  // -------------------------------------------------------------
  // INITIALIZATION
  // -------------------------------------------------------------
  document.addEventListener('DOMContentLoaded', () => {
    fetchPlatformSettings();
    updatePassCountBadge();
    initDivePortal();

    // Load events on Hub & User Portal
    if (page === 'hub' || page === 'user') {
      fetchHackathons();
    } else if (page === 'studio') {
      fetchHackathons().then(() => {
        state.pollInterval = setInterval(pollTelemetry, 2000);
      });
    } else if (page === 'admin') {
      fetchHackathons();
    } else if (page === 'platform') {
      fetchPlatformData();
      state.pollInterval = setInterval(fetchPlatformData, 5000);
    }
  });

  // -------------------------------------------------------------
  // CINEMATIC "DIVE-IN" INTRO PORTAL CONTROLLER
  // -------------------------------------------------------------
  function initDivePortal() {
    const portal = document.getElementById('divePortal');
    if (!portal) return;

    // Automatically dive into the platform after 1.5 seconds
    setTimeout(() => {
      exitDivePortal();
    }, 1500);
  }

  window.exitDivePortal = function () {
    const portal = document.getElementById('divePortal');
    if (!portal || portal.classList.contains('dive-complete')) return;
    portal.classList.add('dive-complete');
    document.body.classList.add('page-loaded-enter');
    setTimeout(() => {
      portal.style.display = 'none';
    }, 850);
  };

  window.replayDivePortal = function () {
    const portal = document.getElementById('divePortal');
    if (!portal) return;
    portal.style.display = 'flex';
    portal.style.filter = 'none';
    portal.style.opacity = '1';
    portal.style.transform = 'scale(1)';
    portal.classList.remove('dive-complete');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    setTimeout(() => {
      exitDivePortal();
    }, 1600);
  };

  // -------------------------------------------------------------
  // CORE API UTILITY
  // -------------------------------------------------------------
  async function api(path, method = 'GET', body = null) {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' }
    };
    if (body) opts.body = JSON.stringify(body);

    const res = await fetch(path, opts);
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message || data.error || `HTTP ${res.status}`);
    }
    return data;
  }

  // -------------------------------------------------------------
  // TOAST NOTIFICATIONS
  // -------------------------------------------------------------
  window.showToast = function (message, type = 'success') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${escapeHtml(message)}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(12px)';
      toast.style.transition = 'all 0.25s ease';
      setTimeout(() => toast.remove(), 250);
    }, 3800);
  };

  // -------------------------------------------------------------
  // FETCH SETTINGS & HACKATHONS
  // -------------------------------------------------------------
  async function fetchPlatformSettings() {
    try {
      const data = await api('/api/settings');
      if (data && data.settings) {
        state.settings = { ...state.settings, ...data.settings };
      }
    } catch (e) {
      // Default fallback
    }
  }

  window.fetchHackathons = async function () {
    try {
      const data = await api('/api/hackathons');
      state.hackathons = data.hackathons || [];
      state.filteredHackathons = [...state.hackathons];

      if (page === 'hub' || page === 'user') {
        renderLuxuryEventCards();
      }
      if (page === 'studio' && typeof populateSimDropdown === 'function') {
        populateSimDropdown();
      }
      if (page === 'admin' && typeof renderHackAdminTable === 'function') {
        renderHackAdminTable();
        populateRosterDropdown();
      }
    } catch (err) {
      console.error('Failed to load hackathons:', err);
      showToast('Connecting to event registry server...', 'warning');
    }
  };

  // -------------------------------------------------------------
  // AVENORA LUXURY CARDS RENDERING (NO UGLY MUTEX LABELS)
  // -------------------------------------------------------------
  function renderLuxuryEventCards() {
    const grid = document.getElementById('eventsGrid');
    if (!grid) return;

    if (!state.filteredHackathons || state.filteredHackathons.length === 0) {
      grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 4.5rem 1rem; background: #FFFFFF; border-radius: 20px; border: 1px dashed var(--border-medium);">
          <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🔍</div>
          <h3 style="font-size: 1.25rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">No Events Match Your Filters</h3>
          <p style="font-size: 0.9rem; color: var(--text-muted); max-width: 420px; margin: 0 auto 1.25rem;">
            Try selecting a different city or category, or clear your search term.
          </p>
          <button class="btn-luxury-outline" onclick="resetFilters()">Reset All Filters</button>
        </div>
      `;
      return;
    }

    grid.innerHTML = state.filteredHackathons.map(event => {
      const remaining = event.remaining_tickets !== undefined ? event.remaining_tickets : (event.tatkal_remaining || 0);
      const total = event.tatkal_quota || event.total_tickets || 4;
      const isSoldOut = remaining <= 0;
      const pct = total > 0 ? Math.max(0, Math.min(100, Math.round((remaining / total) * 100))) : 0;
      
      const isLow = remaining <= 2;
      const spotLabel = isSoldOut 
        ? "Sold Out" 
        : (remaining === 1 ? "Last 1 Squad Pass Remaining!" : `${remaining} Squad Passes Available`);

      return `
        <article class="event-luxury-card" id="event-card-${event.id}">
          <div class="card-media-wrapper">
            <img class="card-media-img" src="${event.image_url || 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=1000&q=80'}" alt="${escapeHtml(event.title)}">
            <div class="card-floating-badge">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
              <span>${escapeHtml(event.city || 'Global Hub')}</span>
            </div>
            <div class="card-date-badge">
              ${escapeHtml(event.dates || '2026-2027')}
            </div>
          </div>

          <div class="card-content">
            <div class="card-category-pill">${escapeHtml(event.category || 'Tech Hackathon')}</div>
            <h3 class="card-title">${escapeHtml(event.title)}</h3>
            <p class="card-tagline">${escapeHtml(event.tagline || 'Collaborate with top engineers on foundation models and distributed infrastructure.')}</p>

            <div class="card-venue-row">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M5 21V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16"></path></svg>
              <span>${escapeHtml(event.venue || 'Hybrid Campus Hub')}</span>
            </div>

            <!-- Capacity Progress (Clean, Commercial, No Ugly Mutex Terms) -->
            <div class="card-capacity-box">
              <div class="card-capacity-header">
                <span class="capacity-label">
                  <span class="dot" style="display:inline-block;width:6px;height:6px;border-radius:50%;background:${isSoldOut ? '#DC2626' : '#059669'};"></span>
                  Reservation Status
                </span>
                <span class="capacity-spots ${isLow ? 'low' : ''}">
                  ${spotLabel}
                </span>
              </div>
              <div class="capacity-track">
                <div class="capacity-fill" style="width: ${pct}%; background: ${isLow ? '#DC2626' : 'var(--text-main)'};"></div>
              </div>
            </div>

            <div class="card-footer">
              <div class="card-price-group">
                <span class="card-price-amount">₹${event.ticket_price || 499}</span>
                <span class="card-price-sub">per squad pass</span>
              </div>
              <button 
                class="btn-book-pass" 
                ${isSoldOut ? 'disabled style="background:#94A3B8;cursor:not-allowed;"' : ''} 
                onclick="openBookingModal(${event.id})"
              >
                ${isSoldOut ? 'Sold Out' : 'Book Team Pass →'}
              </button>
            </div>
          </div>
        </article>
      `;
    }).join('');
  }

  // -------------------------------------------------------------
  // SEARCH & FILTERING (CITY, CATEGORY, KEYWORD)
  // -------------------------------------------------------------
  window.applyFilters = function () {
    const citySelect = document.getElementById('searchCity');
    const categorySelect = document.getElementById('searchCategory');
    const keywordInput = document.getElementById('searchKeyword');

    const selectedCity = citySelect ? citySelect.value : state.activeCityFilter;
    const selectedCategory = categorySelect ? categorySelect.value : state.activeCategoryFilter;
    const keyword = keywordInput ? keywordInput.value.toLowerCase().trim() : '';

    state.activeCityFilter = selectedCity;
    state.activeCategoryFilter = selectedCategory;
    state.searchQuery = keyword;

    state.filteredHackathons = state.hackathons.filter(event => {
      // City check
      let matchesCity = true;
      if (selectedCity && selectedCity !== 'ALL') {
        const cityLower = (event.city || '').toLowerCase();
        matchesCity = cityLower.includes(selectedCity.toLowerCase());
      }

      // Category check
      let matchesCategory = true;
      if (selectedCategory && selectedCategory !== 'ALL') {
        const catLower = (event.category || '').toLowerCase();
        matchesCategory = catLower.includes(selectedCategory.toLowerCase());
      }

      // Keyword check
      let matchesKeyword = true;
      if (keyword) {
        const title = (event.title || '').toLowerCase();
        const tagline = (event.tagline || '').toLowerCase();
        const venue = (event.venue || '').toLowerCase();
        matchesKeyword = title.includes(keyword) || tagline.includes(keyword) || venue.includes(keyword);
      }

      return matchesCity && matchesCategory && matchesKeyword;
    });

    renderLuxuryEventCards();
  };

  window.setQuickCityFilter = function (city, btnElement) {
    state.activeCityFilter = city;
    const citySelect = document.getElementById('searchCity');
    if (citySelect) {
      citySelect.value = city;
    }

    // Update pill active classes
    const pills = document.querySelectorAll('.filter-pill-btn');
    pills.forEach(p => p.classList.remove('active'));
    if (btnElement) {
      btnElement.classList.add('active');
    } else {
      const match = Array.from(pills).find(p => p.getAttribute('data-city') === city);
      if (match) match.classList.add('active');
    }

    applyFilters();

    // Smooth scroll down to events if triggered from destination card
    const eventsSec = document.getElementById('events');
    if (eventsSec) {
      eventsSec.scrollIntoView({ behavior: 'smooth' });
    }
  };

  window.resetFilters = function () {
    const citySelect = document.getElementById('searchCity');
    const categorySelect = document.getElementById('searchCategory');
    const keywordInput = document.getElementById('searchKeyword');

    if (citySelect) citySelect.value = 'ALL';
    if (categorySelect) categorySelect.value = 'ALL';
    if (keywordInput) keywordInput.value = '';

    const pills = document.querySelectorAll('.filter-pill-btn');
    pills.forEach(p => p.classList.remove('active'));
    const allPill = Array.from(pills).find(p => p.getAttribute('data-city') === 'ALL');
    if (allPill) allPill.classList.add('active');

    state.activeCityFilter = 'ALL';
    state.activeCategoryFilter = 'ALL';
    state.searchQuery = '';
    state.filteredHackathons = [...state.hackathons];
    renderLuxuryEventCards();
  };

  // -------------------------------------------------------------
  // SQUAD BOOKING MODAL LOGIC
  // -------------------------------------------------------------
  window.openBookingModal = function (eventId) {
    const event = state.hackathons.find(h => String(h.id) === String(eventId));
    if (!event) {
      showToast('Event information loading, please try again.', 'warning');
      return;
    }

    state.selectedEventForBooking = event;

    const idInput = document.getElementById('bookingEventId');
    const titleEl = document.getElementById('modalEventTitle');
    const metaEl = document.getElementById('modalEventMeta');
    const priceEl = document.getElementById('modalEventPrice');
    const totalEl = document.getElementById('modalTotalVal');
    const membersList = document.getElementById('additionalMembersList');

    if (idInput) idInput.value = event.id;
    if (titleEl) titleEl.innerText = event.title;
    if (metaEl) metaEl.innerText = `${event.city || 'Global Hub'} • ${event.dates || '2026'}`;
    if (priceEl) priceEl.innerText = `₹${event.ticket_price || 499}`;
    if (totalEl) totalEl.innerText = `₹${event.ticket_price || 499}`;

    // Reset member fields
    if (membersList) membersList.innerHTML = '';
    updateMemberCountBadge();

    const modal = document.getElementById('bookingModal');
    if (modal) {
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
      const container = modal.querySelector('.modal-container');
      if (container) container.scrollTop = 0;
    }
  };

  window.closeBookingModal = function () {
    const modal = document.getElementById('bookingModal');
    if (modal) modal.classList.remove('active');
    document.body.style.overflow = '';
  };

  window.addSquadMemberField = function () {
    const list = document.getElementById('additionalMembersList');
    if (!list) return;

    const currentCount = list.children.length;
    if (currentCount >= 3) {
      showToast('Maximum 4 squad members per pass (1 Lead + 3 Members)', 'warning');
      return;
    }

    const row = document.createElement('div');
    row.className = 'squad-member-row';
    row.innerHTML = `
      <input type="text" class="form-input member-name" placeholder="Teammate Name" required>
      <input type="email" class="form-input member-email" placeholder="teammate@sru.edu.in" required>
      <button type="button" class="btn-remove-member" onclick="this.parentElement.remove(); updateMemberCountBadge();" title="Remove">&times;</button>
    `;
    list.appendChild(row);
    updateMemberCountBadge();
  };

  function updateMemberCountBadge() {
    const badge = document.getElementById('memberCountBadge');
    const list = document.getElementById('additionalMembersList');
    if (!badge || !list) return;
    const total = 1 + list.children.length;
    badge.innerText = `${total} / 4 Selected`;
  }

  window.submitBooking = async function (e) {
    e.preventDefault();
    const btn = document.getElementById('submitBookingBtn');
    if (!btn) return;

    btn.disabled = true;
    btn.innerHTML = `<span class="dot" style="width:8px;height:8px;border-radius:50%;background:#fff;display:inline-block;animation:pulse-dot 1s infinite;"></span> Processing Reservation...`;

    const eventId = Number(document.getElementById('bookingEventId').value);
    const teamName = document.getElementById('teamName').value.trim();
    const leaderName = document.getElementById('leaderName').value.trim();
    const leaderEmail = document.getElementById('leaderEmail').value.trim();
    const college = document.getElementById('collegeName').value.trim();
    const leaderHtno = document.getElementById('leaderHtno').value.trim();

    // Squad members
    const memberRows = document.querySelectorAll('#additionalMembersList .squad-member-row');
    const members = [
      { name: leaderName, email: leaderEmail, role: "Team Leader", htno: leaderHtno, college }
    ];

    memberRows.forEach(r => {
      const name = r.querySelector('.member-name').value.trim();
      const email = r.querySelector('.member-email').value.trim();
      if (name) {
        members.push({ name, email, role: "Squad Hacker", college });
      }
    });

    const payload = {
      hackathon_id: eventId,
      team_name: teamName,
      leader_name: leaderName,
      leader_email: leaderEmail,
      members,
      payment_details: {
        method: "razorpay_test_mode",
        gateway_key: state.settings.razorpay_key_id,
        auth_status: "SUCCESS"
      }
    };

    try {
      const res = await api('/api/book', 'POST', payload);
      const booking = res.ticket || res.booking;

      closeBookingModal();
      showToast(`Pass Confirmed! Ticket Code: ${booking.ticket_code}`, 'success');

      // Save pass locally
      savePassLocally(booking, state.selectedEventForBooking);
      updatePassCountBadge();

      // Show Boarding Pass
      renderBoardingPass(booking, state.selectedEventForBooking);

      // Refresh hackathons so remaining spots reflect
      fetchHackathons();
    } catch (err) {
      showToast(err.message || 'Seat unavailable or sold out.', 'danger');
    } finally {
      btn.disabled = false;
      btn.innerText = 'Confirm & Book Pass →';
    }
  };

  // -------------------------------------------------------------
  // PROCEDURAL SVG QR CODE GENERATOR (Pure Client-Side Zero Dependencies)
  // -------------------------------------------------------------
  function generateProceduralSvgQr(text) {
    const size = 21; // 21x21 QR matrix
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
      hash = ((hash << 5) - hash) + text.charCodeAt(i);
      hash |= 0;
    }

    const grid = [];
    for (let r = 0; r < size; r++) {
      grid[r] = [];
      for (let c = 0; c < size; c++) {
        // Standard QR Finder Corners
        const isTopLeft = (r < 7 && c < 7);
        const isTopRight = (r < 7 && c >= size - 7);
        const isBottomLeft = (r >= size - 7 && c < 7);

        if (isTopLeft || isTopRight || isBottomLeft) {
          const lr = isBottomLeft ? r - (size - 7) : r;
          const lc = isTopRight ? c - (size - 7) : c;
          if (lr === 0 || lr === 6 || lc === 0 || lc === 6 || (lr >= 2 && lr <= 4 && lc >= 2 && lc <= 4)) {
            grid[r][c] = 1;
          } else {
            grid[r][c] = 0;
          }
        } else {
          // Pseudorandom deterministic noise based on hash
          const val = Math.abs(Math.sin((r * size + c) + hash)) * 10000;
          grid[r][c] = (val % 2 < 1) ? 1 : 0;
        }
      }
    }

    // Render SVG
    let rects = '';
    const cellSize = 5;
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        if (grid[r][c] === 1) {
          rects += `<rect x="${c * cellSize}" y="${r * cellSize}" width="${cellSize}" height="${cellSize}" fill="#0F172A" />`;
        }
      }
    }

    const totalDim = size * cellSize;
    return `
      <svg viewBox="0 0 ${totalDim} ${totalDim}" xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges">
        <rect width="${totalDim}" height="${totalDim}" fill="#FFFFFF" />
        ${rects}
      </svg>
    `;
  }

  // -------------------------------------------------------------
  // VIP DIGITAL BOARDING PASS
  // -------------------------------------------------------------
  function renderBoardingPass(booking, event) {
    const modal = document.getElementById('passModal');
    if (!modal) return;

    const eventTitle = (event && event.title) || 'Global AI HackSphere 2026';
    const venue = (event && event.venue) || 'Moscone Center, San Francisco';
    const dates = (event && event.dates) || 'Nov 24–26, 2026';

    document.getElementById('passEventTitle').innerText = eventTitle;
    document.getElementById('passVenueText').innerText = `${venue} • ${dates}`;
    document.getElementById('passTeamName').innerText = booking.team_name || 'ByteBusters';
    document.getElementById('passLeaderName').innerText = booking.leader_name || 'Team Leader';

    const squadSize = (booking.members && booking.members.length) || 1;
    document.getElementById('passSquadSize').innerText = `${squadSize} Hacker${squadSize > 1 ? 's' : ''}`;

    const ticketCode = booking.ticket_code || 'TKT-TATKAL-89211';
    document.getElementById('passTicketCode').innerText = ticketCode;
    document.getElementById('passPaymentRef').innerText = `Ref: ${booking.payment_id || 'pay_test_019283'}`;

    // Generate procedural QR
    const qrSvg = generateProceduralSvgQr(ticketCode);
    document.getElementById('passQrContainer').innerHTML = qrSvg;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  window.closePassModal = function () {
    const modal = document.getElementById('passModal');
    if (modal) modal.classList.remove('active');
    document.body.style.overflow = '';
  };

  // -------------------------------------------------------------
  // LOCAL PASS PERSISTENCE & MY PASSES DRAWER
  // -------------------------------------------------------------
  function getStoredPasses() {
    try {
      const syn = localStorage.getItem('synnexa_passes');
      if (syn) return JSON.parse(syn);
      const av = localStorage.getItem('avenora_passes');
      if (av) return JSON.parse(av);
      return [];
    } catch (e) {
      return [];
    }
  }

  function savePassLocally(booking, event) {
    try {
      const existing = getStoredPasses();
      const passRecord = {
        booking,
        event: {
          title: event ? event.title : 'Global Hackathon',
          venue: event ? event.venue : 'Tech Hub',
          city: event ? event.city : 'San Francisco',
          dates: event ? event.dates : '2026'
        },
        savedAt: new Date().toISOString()
      };
      existing.unshift(passRecord);
      localStorage.setItem('synnexa_passes', JSON.stringify(existing));
    } catch (e) {
      console.warn('LocalStorage unavailable', e);
    }
  }

  function updatePassCountBadge() {
    try {
      const existing = getStoredPasses();
      const badge = document.getElementById('userPassCount');
      if (badge) badge.innerText = existing.length;
    } catch (e) {
      // Ignore
    }
  }

  window.openMyPassesModal = function () {
    const modal = document.getElementById('myPassesModal');
    const list = document.getElementById('myPassesList');
    if (!modal || !list) return;

    const passes = getStoredPasses();

    if (passes.length === 0) {
      list.innerHTML = `
        <div style="text-align: center; padding: 3rem 1rem; color: var(--text-muted);">
          <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🎟️</div>
          <div style="font-size: 1.1rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.35rem;">No Passes Reserved Yet</div>
          <p style="font-size: 0.88rem; max-width: 320px; margin: 0 auto 1.25rem;">
            Explore our curated global hackathons and book your squad's verified passes in real time.
          </p>
          <button class="btn-luxury-primary" onclick="closeMyPassesModal()">Explore Events →</button>
        </div>
      `;
    } else {
      list.innerHTML = passes.map((p, idx) => `
        <div style="background:#FFFFFF;border:1px solid var(--border-medium);border-radius:16px;padding:1.25rem;margin-bottom:1rem;display:flex;align-items:center;justify-content:space-between;gap:1rem;box-shadow:var(--shadow-subtle);">
          <div>
            <div style="font-size:0.74rem;font-weight:700;text-transform:uppercase;color:var(--accent-indigo);">${escapeHtml(p.event.city || 'Global Hub')}</div>
            <div style="font-size:1.05rem;font-weight:800;color:var(--text-main);">${escapeHtml(p.event.title)}</div>
            <div style="font-size:0.82rem;color:var(--text-muted);margin-top:0.2rem;">
              Squad: <strong>${escapeHtml(p.booking.team_name)}</strong> • Code: <code style="font-family:var(--font-mono);font-size:0.8rem;background:#F1F5F9;padding:2px 6px;border-radius:4px;">${p.booking.ticket_code}</code>
            </div>
          </div>
          <button class="btn-luxury-outline" onclick="viewStoredPass(${idx})">
            View Pass
          </button>
        </div>
      `).join('');
    }

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  };

  window.closeMyPassesModal = function () {
    const modal = document.getElementById('myPassesModal');
    if (modal) modal.classList.remove('active');
    document.body.style.overflow = '';
  };

  window.viewStoredPass = function (idx) {
    try {
      const passes = JSON.parse(localStorage.getItem('avenora_passes') || '[]');
      const target = passes[idx];
      if (target) {
        closeMyPassesModal();
        renderBoardingPass(target.booking, target.event);
      }
    } catch (e) {
      console.warn('Error displaying stored pass', e);
    }
  };

  // -------------------------------------------------------------
  // HACKATHON ORGANIZER ADMIN INTERFACE
  // -------------------------------------------------------------
  window.renderHackAdminTable = function () {
    const tbody = document.getElementById('hackAdminTableBody');
    if (!tbody) return;

    if (!state.hackathons || state.hackathons.length === 0) {
      tbody.innerHTML = `<tr><td colspan="9" style="text-align:center;padding:2.5rem;color:var(--text-muted);">No active hackathon batches found in catalog.</td></tr>`;
      return;
    }

    tbody.innerHTML = state.hackathons.map(h => {
      const rem = h.remaining_tickets !== undefined ? h.remaining_tickets : (h.tatkal_remaining || 0);
      const quota = h.tatkal_quota !== undefined ? h.tatkal_quota : (h.tatkal_seats || 4);
      const total = h.total_tickets !== undefined ? h.total_tickets : (h.total_seats || 10);

      return `
        <tr>
          <td style="font-family:var(--font-mono);font-size:0.8rem;color:var(--text-muted);">#${h.id}</td>
          <td>
            <div style="font-weight:700;color:var(--text-main);">${escapeHtml(h.title)}</div>
            <div style="font-size:0.75rem;color:var(--text-muted);">${escapeHtml(h.category || 'Tech Track')}</div>
          </td>
          <td>
            <div style="font-size:0.85rem;color:var(--text-main);">${escapeHtml(h.city || 'Global Hub')}</div>
            <div style="font-size:0.75rem;color:var(--text-muted);">${escapeHtml(h.venue || 'Hybrid Campus')}</div>
          </td>
          <td style="font-family:var(--font-mono);font-weight:600;">${total}</td>
          <td style="font-family:var(--font-mono);font-weight:600;color:var(--accent-cyan);">${quota}</td>
          <td>
            <span class="badge ${rem > 0 ? 'badge-success' : 'badge-danger'}">
              ${rem} Left
            </span>
          </td>
          <td style="font-family:var(--font-mono);font-weight:700;">₹${h.ticket_price || 499}</td>
          <td>
            <div style="display:flex;align-items:center;gap:0.6rem;">
              <label class="switch">
                <input type="checkbox" ${h.mutex_enabled ? 'checked' : ''} onchange="toggleLiveMutex(${h.id})">
                <span class="slider"></span>
              </label>
              <span style="font-size:0.75rem;font-weight:700;color:${h.mutex_enabled ? 'var(--accent-emerald)' : '#DC2626'};">
                ${h.mutex_enabled ? 'ON' : 'OFF'}
              </span>
            </div>
          </td>
          <td>
            <button class="btn-luxury-outline" style="padding:0.35rem 0.75rem;font-size:0.78rem;" onclick="selectRosterEvent(${h.id})">
              View Squads
            </button>
          </td>
        </tr>
      `;
    }).join('');
  };

  window.populateRosterDropdown = function () {
    const sel = document.getElementById('rosterFilterSelect');
    if (!sel) return;
    const currentVal = sel.value || 'ALL';
    sel.innerHTML = `
      <option value="ALL">All Events (All Squads)</option>
      ${state.hackathons.map(h => `<option value="${h.id}">${escapeHtml(h.title)}</option>`).join('')}
    `;
    sel.value = currentVal;
    loadRoster(currentVal);
  };

  window.selectRosterEvent = function (eventId) {
    const sel = document.getElementById('rosterFilterSelect');
    if (sel) {
      sel.value = String(eventId);
    }
    loadRoster(eventId);
    const rosterSection = document.getElementById('rosterTableBody');
    if (rosterSection) {
      rosterSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  window.loadRoster = async function (eventId = 'ALL') {
    const tbody = document.getElementById('rosterTableBody');
    const titleEl = document.getElementById('rosterEventTitle');
    if (!tbody) return;

    let targetTitle = 'All Events';
    let url = '/api/teams';

    if (eventId && eventId !== 'ALL') {
      url = `/api/hackathons/${eventId}/teams`;
      const ev = state.hackathons.find(h => h.id === Number(eventId));
      if (ev) targetTitle = ev.title;
    }

    if (titleEl) titleEl.innerText = targetTitle;

    try {
      const data = await api(url);
      const teams = data.teams || [];
      state.currentRoster = teams;

      if (teams.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;padding:2.5rem;color:var(--text-muted);">No squads registered for this event yet.</td></tr>`;
        return;
      }

      tbody.innerHTML = teams.map(t => {
        const membersList = (t.members || []).map(m => m.name || m).join(', ');
        const isCheckedIn = Boolean(t.checked_in);
        const bookedTime = t.booked_at ? new Date(t.booked_at).toLocaleString() : '-';

        return `
          <tr>
            <td>
              <code style="font-family:var(--font-mono);font-size:0.8rem;font-weight:700;background:#F1F5F9;padding:3px 7px;border-radius:4px;color:var(--text-main);">
                ${escapeHtml(t.ticket_code)}
              </code>
            </td>
            <td>
              <strong style="color:var(--text-main);">${escapeHtml(t.team_name)}</strong>
            </td>
            <td>${escapeHtml(t.leader_name)}</td>
            <td style="font-size:0.82rem;color:var(--text-muted);">
              ${escapeHtml(t.leader_email)}
            </td>
            <td style="font-size:0.8rem;max-width:220px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" title="${escapeHtml(membersList)}">
              <span class="badge badge-neutral" style="margin-right:4px;">${(t.members || []).length}</span>
              ${escapeHtml(membersList || t.leader_name)}
            </td>
            <td style="font-family:var(--font-mono);font-size:0.75rem;color:var(--text-muted);">
              ${escapeHtml(t.payment_id || 'rzp_test_pay')}
            </td>
            <td>
              <span class="badge ${isCheckedIn ? 'badge-success' : 'badge-tatkal'}">
                ${isCheckedIn ? 'CHECKED IN' : 'CONFIRMED'}
              </span>
            </td>
            <td style="font-size:0.78rem;color:var(--text-muted);white-space:nowrap;">
              ${bookedTime}
            </td>
          </tr>
        `;
      }).join('');
    } catch (err) {
      console.error('Failed to load roster:', err);
      tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;padding:1.5rem;color:#DC2626;">Failed to load attendee roster.</td></tr>`;
    }
  };

  window.exportRosterCSV = function () {
    const teams = state.currentRoster || [];
    if (teams.length === 0) {
      showToast('No attendee records available to export', 'warning');
      return;
    }

    const headers = ['Ticket Code', 'Squad Name', 'Team Leader', 'Leader Email', 'Squad Size', 'Members', 'Payment Ref', 'Checked In', 'Booked At'];
    const rows = teams.map(t => {
      const membersStr = (t.members || []).map(m => m.name || m).join('; ');
      return [
        `"${t.ticket_code}"`,
        `"${(t.team_name || '').replace(/"/g, '""')}"`,
        `"${(t.leader_name || '').replace(/"/g, '""')}"`,
        `"${t.leader_email || ''}"`,
        (t.members || []).length,
        `"${membersStr.replace(/"/g, '""')}"`,
        `"${t.payment_id || ''}"`,
        t.checked_in ? 'YES' : 'NO',
        `"${t.booked_at || ''}"`
      ].join(',');
    });

    const csvContent = [headers.join(','), ...rows].join('\r\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `synnexa_roster_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast('Attendee roster CSV exported successfully', 'success');
  };

  // Admin Modals
  window.openNewBatchModal = function () {
    const modal = document.getElementById('modalNewBatch');
    if (modal) modal.classList.add('active');
  };

  window.closeNewBatchModal = function () {
    const modal = document.getElementById('modalNewBatch');
    if (modal) modal.classList.remove('active');
  };

  window.handleCreateBatch = async function (e) {
    e.preventDefault();
    const title = document.getElementById('batchTitle').value.trim();
    const city = document.getElementById('batchCity').value.trim();
    const category = document.getElementById('batchCategory').value.trim();
    const venue = document.getElementById('batchVenue').value.trim();
    const dates = document.getElementById('batchDates').value.trim();
    const price = Number(document.getElementById('batchPrice').value);
    const tatkalSeats = Number(document.getElementById('batchTatkalSeats').value);
    const desc = document.getElementById('batchDesc').value.trim();
    const imageUrl = document.getElementById('batchImageUrl').value.trim();
    const mutexEnabled = document.getElementById('batchMutexToggle').checked;

    try {
      await api('/api/hackathons', 'POST', {
        title,
        city,
        category,
        venue,
        dates,
        ticket_price: price,
        tatkal_quota: tatkalSeats,
        tagline: desc,
        image_url: imageUrl,
        mutex_enabled: mutexEnabled
      });

      showToast(`Batch "${title}" published to catalog!`, 'success');
      closeNewBatchModal();
      document.getElementById('newBatchForm').reset();
      fetchHackathons();
    } catch (err) {
      showToast(err.message || 'Failed to create ticket batch', 'danger');
    }
  };

  window.openCheckInModal = function () {
    const modal = document.getElementById('modalCheckIn');
    const box = document.getElementById('checkInResultBox');
    if (box) box.style.display = 'none';
    const input = document.getElementById('checkInCode');
    if (input) input.value = '';
    if (modal) modal.classList.add('active');
  };

  window.closeCheckInModal = function () {
    const modal = document.getElementById('modalCheckIn');
    if (modal) modal.classList.remove('active');
  };

  window.handleDoorCheckIn = async function (e) {
    e.preventDefault();
    const codeInput = document.getElementById('checkInCode');
    const box = document.getElementById('checkInResultBox');
    if (!codeInput || !box) return;

    const ticketCode = codeInput.value.trim().toUpperCase();

    try {
      const res = await api('/api/hackathons/checkin', 'POST', { ticket_code: ticketCode });
      box.style.display = 'block';
      box.style.background = '#ECFDF5';
      box.style.border = '1px solid #A7F3D0';
      box.style.color = '#065F46';
      box.innerHTML = `
        <strong>✓ Access Granted</strong><br>
        Squad: <strong>${escapeHtml(res.team ? res.team.team_name : 'Hacker Squad')}</strong><br>
        Leader: ${escapeHtml(res.team ? res.team.leader_name : '-')}<br>
        Admitted to venue at ${new Date().toLocaleTimeString()}
      `;
      showToast('Participant successfully checked in', 'success');
      const sel = document.getElementById('rosterFilterSelect');
      loadRoster(sel ? sel.value : 'ALL');
    } catch (err) {
      box.style.display = 'block';
      box.style.background = '#FEF2F2';
      box.style.border = '1px solid #FECACA';
      box.style.color = '#991B1B';
      box.innerHTML = `<strong>✗ Check-In Rejected:</strong> ${escapeHtml(err.message)}`;
    }
  };

  // -------------------------------------------------------------
  // PLATFORM ADMIN & TELEMETRY CONTROLS
  // -------------------------------------------------------------
  window.fetchPlatformData = async function () {
    try {
      // 1. Fetch Stats
      const statsRes = await api('/api/platform/stats');
      if (statsRes && statsRes.stats) {
        const s = statsRes.stats;
        const elEv = document.getElementById('statTotalEvents');
        const elTm = document.getElementById('statTotalTeams');
        const elRev = document.getElementById('statTotalRevenue');
        const elLck = document.getElementById('statTotalLocks');
        const elCon = document.getElementById('statTotalContentions');

        if (elEv) elEv.innerText = s.total_events || 0;
        if (elTm) elTm.innerText = s.total_teams_registered || 0;
        if (elRev) elRev.innerText = `₹${(s.total_revenue_inr || 0).toLocaleString()}`;
        if (elLck) elLck.innerText = s.total_lock_acquisitions || 0;
        if (elCon) elCon.innerText = s.total_contentions_handled || 0;
      }

      // 2. Fetch Settings if not prefilled
      if (!state.isSettingsLoaded) {
        loadPlatformSettings();
      }

      // 3. Fetch Audit Logs
      const logsRes = await api('/api/audit-logs?limit=50');
      const tbody = document.getElementById('auditTableBody');
      if (tbody && logsRes.logs) {
        if (logsRes.logs.length === 0) {
          tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:2.5rem;color:var(--text-muted);">No critical section transactions logged yet.</td></tr>`;
          return;
        }

        tbody.innerHTML = logsRes.logs.map(l => {
          const isSuccess = l.status === 'SUCCESS';
          const time = l.timestamp ? new Date(l.timestamp).toLocaleTimeString() : '-';
          const detailsStr = l.details ? JSON.stringify(l.details) : '';

          return `
            <tr>
              <td style="font-family:var(--font-mono);font-size:0.75rem;color:var(--text-muted);white-space:nowrap;">
                ${time}
              </td>
              <td>
                <span class="badge ${l.action.includes('LOCK') || l.action.includes('MUTEX') ? 'badge-tatkal' : 'badge-neutral'}">
                  ${escapeHtml(l.action)}
                </span>
              </td>
              <td style="font-family:var(--font-mono);font-size:0.8rem;">
                ${l.hackathon_id ? '#' + l.hackathon_id : '-'}
              </td>
              <td>
                <strong style="font-size:0.82rem;color:var(--text-main);">${escapeHtml(l.team_name || '-')}</strong>
              </td>
              <td>
                <span class="badge ${isSuccess ? 'badge-success' : 'badge-danger'}">
                  ${l.status}
                </span>
              </td>
              <td style="font-family:var(--font-mono);font-size:0.75rem;">
                ${l.duration_ms !== undefined ? l.duration_ms + 'ms' : '-'}
              </td>
              <td style="font-family:var(--font-mono);font-size:0.72rem;color:var(--text-muted);max-width:320px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${escapeHtml(detailsStr)}">
                ${escapeHtml(detailsStr || '-')}
              </td>
            </tr>
          `;
        }).join('');
      }
    } catch (err) {
      console.error('Failed to load platform data:', err);
    }
  };

  window.loadPlatformSettings = async function () {
    try {
      const data = await api('/api/settings');
      if (data && data.settings) {
        state.settings = data.settings;
        state.isSettingsLoaded = true;

        const kId = document.getElementById('rzpKeyId');
        const kSec = document.getElementById('rzpKeySecret');
        const fee = document.getElementById('platformFee');
        const curr = document.getElementById('rzpCurrency');
        const hook = document.getElementById('rzpWebhook');

        if (kId) kId.value = data.settings.razorpay_key_id || 'rzp_test_1DP5mmOlF5G5ag';
        if (kSec) kSec.value = data.settings.razorpay_key_secret || 'test_secret_synnexa_2026';
        if (fee) fee.value = data.settings.platform_fee || 0;
        if (curr) curr.value = data.settings.currency || 'INR';
        if (hook) hook.value = data.settings.webhook_secret || '';
      }
    } catch (e) {
      console.warn('Could not load settings', e);
    }
  };

  window.savePlatformSettings = async function (e) {
    if (e) e.preventDefault();
    const kId = document.getElementById('rzpKeyId').value.trim();
    const kSec = document.getElementById('rzpKeySecret').value.trim();
    const fee = Number(document.getElementById('platformFee').value || 0);
    const curr = document.getElementById('rzpCurrency').value;
    const hook = document.getElementById('rzpWebhook').value.trim();

    try {
      const res = await api('/api/settings', 'POST', {
        razorpay_key_id: kId,
        razorpay_key_secret: kSec,
        platform_fee: fee,
        currency: curr,
        webhook_secret: hook
      });

      state.settings = res.settings;
      showToast('Platform settings & Razorpay test credentials updated successfully!', 'success');
    } catch (err) {
      showToast(err.message || 'Failed to save settings', 'danger');
    }
  };

  window.clearAuditLogs = async function () {
    try {
      await api('/api/audit-logs/clear', 'POST');
      showToast('Critical section audit trail cleared', 'success');
      fetchPlatformData();
    } catch (err) {
      showToast(err.message || 'Failed to clear logs', 'danger');
    }
  };

  // -------------------------------------------------------------
  // STUDIO & CONCURRENCY BENCHMARK CONTROLS
  // -------------------------------------------------------------
  window.populateSimDropdown = function () {
    const select = document.getElementById('simEventSelect');
    if (!select) return;
    select.innerHTML = state.hackathons.map(h => {
      const rem = h.remaining_tickets !== undefined ? h.remaining_tickets : (h.tatkal_remaining || 0);
      return `<option value="${h.id}">${escapeHtml(h.title)} (${rem} seats left)</option>`;
    }).join('');
    onSimEventChange();
  };

  window.onSimEventChange = function () {
    const sel = document.getElementById('simEventSelect');
    if (!sel) return;
    const ev = state.hackathons.find(h => h.id === Number(sel.value));
    if (ev) {
      const rem = ev.remaining_tickets !== undefined ? ev.remaining_tickets : (ev.tatkal_remaining || 0);
      const seatsEl = document.getElementById('telemSeats');
      if (seatsEl) seatsEl.innerText = rem;
    }
  };

  window.onMutexToggleChange = function () {
    const toggle = document.getElementById('simMutexToggle');
    const lbl = document.getElementById('mutexModeLabel');
    const desc = document.getElementById('mutexModeDesc');
    if (!toggle || !lbl || !desc) return;

    if (toggle.checked) {
      lbl.innerText = 'Mutex Barrier Active (Atomic FIFO)';
      lbl.style.color = 'var(--accent-emerald)';
      desc.innerText = 'Requests are serialized via an asynchronous FIFO queue. Strict mutual exclusion, bounded waiting, zero overbooking guarantee.';
    } else {
      lbl.innerText = 'Mutex Barrier Disabled (Race Condition Hazard)';
      lbl.style.color = '#DC2626';
      desc.innerText = 'Unprotected execution path. Simultaneous dirty reads will cause seat reservations to exceed available capacity (overselling bug).';
    }
  };

  window.triggerConcurrentRush = async function () {
    const btn = document.getElementById('btnRunRush');
    const sel = document.getElementById('simEventSelect');
    const range = document.getElementById('simThreadsRange');
    const toggle = document.getElementById('simMutexToggle');
    const term = document.getElementById('terminalOutput');

    if (!btn || !sel || !range) return;

    const eventId = Number(sel.value);
    const numTeams = Number(range.value);
    const withMutex = toggle ? toggle.checked : true;

    btn.disabled = true;
    btn.innerHTML = `<span class="dot" style="width:8px;height:8px;border-radius:50%;background:#fff;display:inline-block;animation:pulse-dot 1s infinite;"></span> Simulating ${numTeams} Concurrent Squad Requests...`;

    if (term) {
      term.innerText = `[RUSH_INIT] Spawning ${numTeams} concurrent asynchronous requests against Event #${eventId}...\n[BARRIER] Mutex Concurrency Protection: ${withMutex ? 'ENABLED (FIFO Serialized)' : 'DISABLED (TOCTOU Hazard Exposed)'}\n[START] Submitting burst at ${new Date().toISOString()}...\n`;
    }

    try {
      const res = await api('/api/simulate-rush', 'POST', {
        hackathon_id: eventId,
        num_teams: numTeams,
        with_mutex: withMutex
      });

      const summary = res.summary || res;

      // Update Terminal
      if (term) {
        let logLines = `[RUSH_COMPLETED] Execution finished in ${summary.duration_ms || 12}ms\n`;
        logLines += `--------------------------------------------------------\n`;
        logLines += `• Initial Capacity:   ${summary.initial_seats} seats\n`;
        logLines += `• Final Capacity:     ${summary.final_seats} seats\n`;
        logLines += `• Successful Passes:  ${summary.successful_bookings} squads\n`;
        logLines += `• Rejected Passes:    ${summary.rejected_bookings} squads\n`;
        logLines += `• Overselling Count:  ${summary.excess_oversold} tickets\n`;
        logLines += `• Mutex Invariant:    ${summary.overbooking_detected ? 'VIOLATED (NEGATIVE SEATS / OVERBOOKING DETECTED)' : 'INTACT (100% MUTUAL EXCLUSION ENFORCED)'}\n\n`;
        logLines += `[MICROSECOND LOGS]:\n`;

        if (summary.logs && summary.logs.length) {
          summary.logs.forEach(l => {
            logLines += `[${(l.timestamp || '').slice(11, 23)}] [${l.action}] ${l.team_name} -> ${l.status} (${l.details || ''})\n`;
          });
        }
        term.innerText = logLines;
        term.scrollTop = term.scrollHeight;
      }

      // Update Scorecard
      const scMode = document.getElementById('scoreMode');
      const scInit = document.getElementById('scoreInitial');
      const scFin = document.getElementById('scoreFinal');
      const scSucc = document.getElementById('scoreSuccess');
      const scOver = document.getElementById('scoreOversell');
      const scInv = document.getElementById('scoreInvariant');

      if (scMode) scMode.innerText = withMutex ? 'Protected' : 'Unprotected';
      if (scInit) scInit.innerText = summary.initial_seats;
      if (scFin) scFin.innerText = summary.final_seats;
      if (scSucc) scSucc.innerText = summary.successful_bookings;
      if (scOver) {
        scOver.innerText = summary.excess_oversold;
        scOver.style.color = summary.excess_oversold > 0 ? '#DC2626' : 'var(--text-main)';
      }
      if (scInv) {
        scInv.innerText = summary.overbooking_detected ? 'VIOLATED' : 'INTACT';
        scInv.style.color = summary.overbooking_detected ? '#DC2626' : 'var(--accent-emerald)';
      }

      // Update Telemetry Header
      const seatsEl = document.getElementById('telemSeats');
      if (seatsEl) seatsEl.innerText = summary.final_seats;

      if (summary.overbooking_detected) {
        showToast(`Race condition triggered! ${summary.excess_oversold} excess tickets oversold (TOCTOU hazard confirmed).`, 'danger');
      } else {
        showToast(`Rush verified! ${summary.successful_bookings} passes granted, exactly 0 overbooking. Mutex invariant intact.`, 'success');
      }

      fetchHackathons();
    } catch (err) {
      showToast(err.message || 'Concurrency simulation failed', 'danger');
    } finally {
      btn.disabled = false;
      btn.innerHTML = `
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
        </svg>
        Fire Tatkal Concurrent Rush
      `;
    }
  };

  window.toggleLiveMutex = async function (eventId) {
    try {
      const res = await api(`/api/hackathons/${eventId}/toggle-mutex`, 'POST');
      showToast(res.message, 'success');
      fetchHackathons();
    } catch (err) {
      showToast(err.message, 'danger');
    }
  };

  window.resetSystemState = async function () {
    try {
      const res = await api('/api/reset-all', 'POST');
      showToast('System reset to baseline with international hackathons (2 Tatkal seats remaining)', 'success');
      fetchHackathons();
      if (page === 'studio') {
        const term = document.getElementById('terminalOutput');
        if (term) term.innerText = `[RESET] System baseline restored with 2 Tatkal seats and pristine Mutex barriers.`;
        const scMode = document.getElementById('scoreMode');
        const scInit = document.getElementById('scoreInitial');
        const scFin = document.getElementById('scoreFinal');
        const scSucc = document.getElementById('scoreSuccess');
        const scOver = document.getElementById('scoreOversell');
        const scInv = document.getElementById('scoreInvariant');
        if (scMode) scMode.innerText = 'Baseline Ready';
        if (scInit) scInit.innerText = '2';
        if (scFin) scFin.innerText = '2';
        if (scSucc) scSucc.innerText = '—';
        if (scOver) scOver.innerText = '0';
        if (scInv) scInv.innerText = 'INTACT';
      }
    } catch (err) {
      showToast(err.message, 'danger');
    }
  };

  async function pollTelemetry() {
    try {
      const data = await api('/api/mutex-state');
      if (data && data.snapshots) {
        const lockEl = document.getElementById('telemLockState');
        const queueEl = document.getElementById('telemQueue');
        const sel = document.getElementById('simEventSelect');
        const targetId = sel ? sel.value : '1';
        const targetSnap = data.snapshots[targetId];

        if (targetSnap) {
          if (lockEl) {
            lockEl.innerHTML = targetSnap.isLocked
              ? `<span class="badge badge-danger" style="font-size:0.8rem;">LOCKED</span>`
              : `<span class="badge badge-success" style="font-size:0.8rem;">UNLOCKED</span>`;
          }
          if (queueEl) {
            queueEl.innerHTML = `${targetSnap.queueLength} <span style="font-size:0.75rem; color:var(--text-muted); font-weight:normal;">threads</span>`;
          }
        }
      }
    } catch (e) {
      // Ignore poll error
    }
  }

  // -------------------------------------------------------------
  // GLOBAL MODAL BACKDROP & ESCAPE CONTROLS
  // -------------------------------------------------------------
  document.addEventListener('click', (e) => {
    if (e.target && e.target.classList.contains('modal-backdrop')) {
      e.target.classList.remove('active');
      document.body.style.overflow = '';
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-backdrop.active').forEach(m => {
        m.classList.remove('active');
      });
      document.body.style.overflow = '';
    }
  });

  // -------------------------------------------------------------
  // HTML ESCAPING SANITIZER
  // -------------------------------------------------------------
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

})();
