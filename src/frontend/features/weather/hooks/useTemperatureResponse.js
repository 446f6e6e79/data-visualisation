import { fetchStatsByWeather } from "../services/statsByWeatherApi.js";
import useApiQueryWithFilters from "../../../clients/baseApiQuery.js";

/**
 * Fetch rides-per-hour bucketed by temperature for the population selected in the global header.
 * @returns Temperature bins, the active user type, and status fields.
 */
function useTemperatureResponse(filters = {}) {
    const params = { ...filters, variable: "temperature", group_by: "none" };

    const query = useApiQueryWithFilters({
        queryKey: "temperature-response",
        fetcher: fetchStatsByWeather,
        filters: params,
    });

    return {
        bins: query.data,
        userType: filters.user_type ?? null,
        loading: query.loading,
        error: query.error,
        refetch: query.refetch,
        isFetching: query.isFetching,
    };
}

export default useTemperatureResponse;
