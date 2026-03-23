const state = {
    currentView: 'melon',
    melonType: 'realtime',
    crossServices: ['melon', 'bugs', 'genie'],
};

const dom = {
    refreshBtn: document.getElementById('refreshBtn'),
    toggleSourceBtn: document.getElementById('toggleSourceBtn'),

    loadingSpinner: document.getElementById('loadingSpinner'),
    errorMessage: document.getElementById('errorMessage'),

    chartGrid: document.querySelector('.chart-grid'),
    melonChartPanel: document.getElementById('melonCharts'),
    melonChartList: document.getElementById('melonChartList'),
    melonChartTitle: document.getElementById('melonChartTitle'),
    koreaChartPanel: document.getElementById('koreaCharts'),
    crossChartList: document.getElementById('crossPlatformChart'),
    serviceSummary: document.getElementById('serviceSummary'),

    totalTracks: document.getElementById('totalTracks'),
    koreaCount: document.getElementById('koreaCount'),
    globalCount: document.getElementById('globalCount'),
    lastUpdated: document.getElementById('lastUpdated'),
    crossPlatformHitsValue: document.getElementById('crossPlatformHitsValue'),
    crossServicesMeta: document.getElementById('crossServicesMeta'),
    successRateValue: document.getElementById('successRateValue'),
    crossLastUpdated: document.getElementById('crossLastUpdated'),

    sourceButtons: document.querySelectorAll('.source-btn'),
    melonTypeButtons: document.querySelectorAll('.melon-type-btn'),
    koreaServiceButtons: document.querySelectorAll('.korea-service-btn'),
};

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    switchView('melon');
});

function setupEventListeners() {
    dom.refreshBtn?.addEventListener('click', () => loadCurrentView());
    dom.toggleSourceBtn?.addEventListener('click', () => {
        const nextView = state.currentView === 'melon' ? 'cross' : 'melon';
        switchView(nextView);
    });

    dom.sourceButtons.forEach(btn => {
        btn.addEventListener('click', () => switchView(btn.dataset.source));
    });

    dom.melonTypeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            state.melonType = btn.dataset.type;
            setActiveButton(dom.melonTypeButtons, btn);
            loadMelonChart();
        });
    });

    dom.koreaServiceButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            state.crossServices = btn.dataset.services.split(',').map(name => name.trim()).filter(Boolean);
            setActiveButton(dom.koreaServiceButtons, btn);
            if (state.currentView === 'cross') {
                loadCrossCharts();
            }
        });
    });
}

function switchView(view) {
    if (state.currentView === view) {
        loadCurrentView();
        return;
    }

    state.currentView = view;
    setActiveButton(dom.sourceButtons, Array.from(dom.sourceButtons).find(btn => btn.dataset.source === view));

    if (view === 'melon') {
        dom.melonChartPanel.classList.remove('hidden');
        dom.koreaChartPanel.classList.add('hidden');
    } else {
        dom.melonChartPanel.classList.add('hidden');
        dom.koreaChartPanel.classList.remove('hidden');
    }

    loadCurrentView();
}

function setActiveButton(buttonList, activeButton) {
    buttonList.forEach(btn => btn.classList.remove('active'));
    if (activeButton) {
        activeButton.classList.add('active');
    }
}

function loadCurrentView() {
    if (state.currentView === 'melon') {
        loadMelonChart();
    } else {
        loadCrossCharts();
    }
}

async function loadMelonChart() {
    showLoading(true);
    hideError();

    try {
        const response = await fetch(`/api/melon/charts?type=${state.melonType}&limit=50`);
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || '멜론 차트 데이터를 가져오지 못했습니다.');
        }

        const tracks = data.chart_data?.tracks || [];
        renderMelonTracks(tracks);
        updateMelonStats(data, tracks.length);
        dom.melonChartTitle.textContent = `Melon ${state.melonType.replace('_', ' ').toUpperCase()} TOP 50`;
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

function renderMelonTracks(tracks) {
    if (!dom.melonChartList) return;
    if (!tracks.length) {
        dom.melonChartList.innerHTML = '<p class="track-title">데이터가 없습니다.</p>';
        return;
    }

    const html = tracks.map((track, index) => {
        const rank = track.rank || index + 1;
        const thumbnail = track.thumbnail || '';
        const title = escapeHtml(track.title || 'Unknown Track');
        const artist = escapeHtml(track.artist || 'Unknown Artist');
        const album = track.album && track.album !== '알 수 없음' ? `<div class="track-artist">${escapeHtml(track.album)}</div>` : '';
        return `
            <div class="track-card">
                <div class="track-rank">#${rank}</div>
                ${thumbnail ? `<img src="${thumbnail}" alt="Album Cover">` : '<div class="track-thumbnail" style="width:56px;height:56px;border-radius:12px;background:rgba(255,255,255,0.08);"></div>'}
                <div class="track-info">
                    <div class="track-title">${title}</div>
                    <div class="track-artist">${artist}</div>
                    ${album}
                </div>
                <div class="track-meta">
                    <span>Melon</span>
                    <small>${track.chart_type || 'Realtime'}</small>
                </div>
            </div>
        `;
    }).join('');

    dom.melonChartList.innerHTML = html;
}

function updateMelonStats(data, trackCount) {
    dom.totalTracks && (dom.totalTracks.textContent = data.total_tracks || trackCount || '-');
    dom.koreaCount && (dom.koreaCount.textContent = trackCount || '-');
    dom.globalCount && (dom.globalCount.textContent = '-');
    if (dom.lastUpdated) {
        const timestamp = data.timestamp ? new Date(data.timestamp) : new Date();
        dom.lastUpdated.textContent = timestamp.toLocaleTimeString('ko-KR');
    }
}

async function loadCrossCharts() {
    showLoading(true);
    hideError();

    try {
        const params = new URLSearchParams();
        state.crossServices.forEach(service => params.append('services', service));
        params.append('limit', '50');

        const response = await fetch(`/api/korea-charts/all?${params.toString()}`);
        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || '통합 차트 데이터를 불러오지 못했습니다.');
        }

        renderCrossHits(data.cross_platform_analysis?.cross_platform_hits || []);
        renderServiceSummary(data.services || {});
        updateCrossHighlights(data);
        dom.totalTracks && (dom.totalTracks.textContent = data.total_tracks || '-');
        dom.koreaCount && (dom.koreaCount.textContent = data.successful_services || state.crossServices.length);
        dom.globalCount && (dom.globalCount.textContent = (data.total_services || state.crossServices.length) - (data.successful_services || 0));
        const timestamp = data.timestamp ? new Date(data.timestamp) : new Date();
        dom.lastUpdated && (dom.lastUpdated.textContent = timestamp.toLocaleTimeString('ko-KR'));
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

function renderCrossHits(hits) {
    if (!dom.crossChartList) return;
    if (!hits.length) {
        dom.crossChartList.innerHTML = '<p class="track-title">크로스 플랫폼 히트곡이 없습니다.</p>';
        return;
    }

    const html = hits.slice(0, 10).map((hit, index) => `
        <div class="cross-hit-card">
            <div class="track-rank">#${index + 1}</div>
            <div>
                <div class="cross-hit-title">${escapeHtml(hit.title)}</div>
                <div class="track-artist">${escapeHtml(hit.artist)}</div>
                <div class="cross-hit-services">${escapeHtml((hit.services || []).join(', '))}</div>
            </div>
            <div class="track-meta">
                <span>${hit.services_count || 0} services</span>
                <small>Score ${Math.round(hit.cross_platform_score || 0)}</small>
            </div>
        </div>
    `).join('');

    dom.crossChartList.innerHTML = html;
}

function renderServiceSummary(services) {
    if (!dom.serviceSummary) return;
    const nameMap = { melon: 'Melon', bugs: 'Bugs', genie: 'Genie', vibe: 'Vibe', flo: 'Flo' };
    const rows = Object.entries(services).map(([service, data]) => {
        const label = nameMap[service] || service;
        const realtime = data.realtime || {};
        const count = realtime.total_tracks || realtime.tracks?.length || 0;
        return `
            <div class="service-row">
                <span>${label}</span>
                <span>${count} tracks</span>
            </div>
        `;
    });
    dom.serviceSummary.innerHTML = rows.join('') || '<div class="service-row">서비스 데이터가 없습니다.</div>';
}

function updateCrossHighlights(data) {
    const hits = data.cross_platform_analysis?.cross_platform_hits || [];
    dom.crossPlatformHitsValue && (dom.crossPlatformHitsValue.textContent = hits.length ? hits.length : '-');
    dom.successRateValue && (dom.successRateValue.textContent = `${Math.round(data.success_rate || 0)}%`);
    dom.crossServicesMeta && (dom.crossServicesMeta.textContent = `Services: ${state.crossServices.length}`);
    if (dom.crossLastUpdated) {
        const timestamp = data.timestamp ? new Date(data.timestamp) : new Date();
        dom.crossLastUpdated.textContent = timestamp.toLocaleString('ko-KR');
    }
}

function showLoading(active) {
    if (dom.loadingSpinner) {
        dom.loadingSpinner.classList.toggle('hidden', !active);
    }
    if (dom.chartGrid) {
        dom.chartGrid.style.opacity = active ? '0.4' : '1';
    }
    if (dom.refreshBtn) {
        dom.refreshBtn.disabled = active;
        dom.refreshBtn.textContent = active ? '⏳ 로딩중...' : 'Refresh_Data';
    }
}

function showError(message) {
    if (!dom.errorMessage) return;
    dom.errorMessage.textContent = message;
    dom.errorMessage.classList.remove('hidden');
    dom.chartGrid && (dom.chartGrid.style.opacity = '0.5');
}

function hideError() {
    if (!dom.errorMessage) return;
    dom.errorMessage.classList.add('hidden');
    dom.chartGrid && (dom.chartGrid.style.opacity = '1');
}

function escapeHtml(value) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return value ? value.replace(/[&<>"']/g, m => map[m]) : '';
}

console.log('[Charts] 모듈 로딩 완료');
