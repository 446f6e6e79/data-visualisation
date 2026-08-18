import { useMemo } from 'react'
import useChartJs from '@/hooks/useChartJs.js'
import {
    formatTemperaturePoints,
    buildTemperatureResponseConfig,
} from '../utils/temperatureResponseConfig.js'

/**
 * Handler hook for the temperature-response line chart: shapes the temperature bins and wires the Chart.js canvas.
 * @param {Object} params
 * @param {Array} params.bins - Temperature bins from useTemperatureResponse.
 * @param {string|null} params.userType - Active header user type, or null for every rider.
 * @returns {{canvasRef: Object, hasData: boolean}} Canvas ref and whether the series has points.
 */
export default function useTemperatureResponseChart({ bins, userType }) {
    const points = useMemo(() => formatTemperaturePoints(bins), [bins])
    const hasData = points.length > 0

    const { canvasRef } = useChartJs({
        buildConfig: () => buildTemperatureResponseConfig(points, userType),
        structuralKey: useMemo(() => JSON.stringify({ points, userType }), [points, userType]),
    })

    return { canvasRef, hasData }
}
