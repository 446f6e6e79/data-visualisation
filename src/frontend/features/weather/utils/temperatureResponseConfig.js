import {
    ACCENT,
    INK,
    INK_MUTED,
    RULE,
    FONT_SANS,
    FONT_MONO,
} from '@/utils/editorialTokens.js'
import { formatNumber } from '@/utils/numberFormat.js'
import { RIDE_METRIC_LABELS } from '@/utils/rideMetricLabels.js'

// Bins with fewer hours are dropped to avoid a wild single-hour outlier point.
const MIN_HOURS = 5
// Temperature is bucketed per whole degree in the backend (_WEATHER_EXPRS in src/backend/services/ride_stats.py), so each point stands for one degree.

const USER_TYPE_LABELS = { member: 'Members', casual: 'Casual riders' }
const ALL_RIDERS_LABEL = 'All riders'

/**
 * Converts temperature-bin stats into sorted rides-per-hour points, dropping
 * bins with too few covered hours to be meaningful.
 * @param {Array} bins - Temperature bins from the fetch hook.
 * @returns {Array} [{x, y}] sorted by temperature.
 */
export function formatTemperaturePoints(bins) {
    return bins
        .filter((bin) => bin.weather_bin !== null && bin.hours_count >= MIN_HOURS)
        .map((bin) => ({ x: Number(bin.weather_bin), y: bin.total_rides / bin.hours_count }))
        .sort((a, b) => a.x - b.x)
}

/**
 * Builds the Chart.js config for the temperature-response line chart: average
 * rides per hour across temperature bins for the population the header selects.
 * @param {Array} points - Points shaped by formatTemperaturePoints.
 * @param {string|null} userType - Active header user type, or null for every rider.
 * @returns {Object} The Chart.js config.
 */
export function buildTemperatureResponseConfig(points, userType) {
    return {
        type: 'line',
        data: {
            datasets: [{
                label: USER_TYPE_LABELS[userType] ?? ALL_RIDERS_LABEL,
                data: points,
                borderColor: ACCENT,
                backgroundColor: ACCENT,
                borderWidth: 2,
                pointRadius: 2.5,
                tension: 0.25,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { family: FONT_MONO, size: 10 },
                        color: INK_MUTED,
                        boxWidth: 12,
                        boxHeight: 12,
                        padding: 16,
                    },
                },
                tooltip: {
                    callbacks: {
                        title: (items) => `${items[0].parsed.x}°C`,
                        label: (item) => `${item.dataset.label}: ${formatNumber(item.parsed.y, 2)} ${RIDE_METRIC_LABELS.perHour.unit}`,
                    },
                },
            },
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Temperature (°C)',
                        font: { family: FONT_SANS, size: 13, weight: '500' },
                        color: INK,
                    },
                    ticks: {
                        font: { family: FONT_MONO, size: 10 },
                        color: INK_MUTED,
                        callback: (value) => `${value}°`,
                    },
                    grid: { color: RULE },
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: RIDE_METRIC_LABELS.perHour.label,
                        font: { family: FONT_SANS, size: 13, weight: '500' },
                        color: INK,
                    },
                    ticks: {
                        font: { family: FONT_MONO, size: 10 },
                        color: INK_MUTED,
                        callback: (value) => Number(value).toFixed(0),
                    },
                    grid: { color: RULE },
                },
            },
        },
    }
}
