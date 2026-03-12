import pandas as pd
from routes import stats
from models.stats import DailyStats, RideTypeStats, Stats, UserTypeStats
from models.ride import RideableType, MemberCasual

def _compute_base_stats(rides: pd.DataFrame) -> Stats:
    return Stats(
        total_rides=len(rides),
        average_duration_seconds=rides['trip_duration'].mean(),
        average_distance_km=rides['trip_distance'].mean(),
        total_duration_seconds=rides['trip_duration'].sum(),
        total_distance_km=rides['trip_distance'].sum()
    )
def compute_all_ride_type_stats(df: pd.DataFrame) -> list[RideTypeStats]:
    """Compute statistics for all rideable types"""
    return [compute_ride_type_stats(df, rideable_type) for rideable_type in RideableType]

def compute_ride_type_stats(df: pd.DataFrame, rideable_type: RideableType) -> RideTypeStats:
    """Compute statistics for a specific rideable type"""
    rides = df[df['rideable_type'] == rideable_type.value]
    return RideTypeStats(
        rideable_type=rideable_type,
        stats=_compute_base_stats(rides)
    )

def compute_all_user_type_stats(df: pd.DataFrame) -> list[UserTypeStats]:
    """Compute statistics for all user types"""
    return [compute_user_type_stats(df, user_type) for user_type in MemberCasual]

def compute_user_type_stats(df: pd.DataFrame, user_type: MemberCasual) -> UserTypeStats:
    """Compute statistics for a specific user type"""
    rides = df[df['member_casual'] == user_type.value]
    return UserTypeStats(
        user_type=user_type,
        stats=_compute_base_stats(rides)
    )

def compute_daily_stats(df: pd.DataFrame) -> list[DailyStats]:
    """Compute statistics for each day of the week."""
    daily_stats = []
    for day in sorted(df['start_day_of_week'].unique()):
        # Count the number of days in the dataset for this day of the week to compute average rides per day
        days_count = len(df[df['start_day_of_week'] == day])
        # Filter rides for the current day of the week
        rides = df[df['start_day_of_week'] == day]
        
        daily_stats.append(
            DailyStats(
                day_of_week=day,
                stats=_compute_base_stats(rides),
            )
        )
    return daily_stats