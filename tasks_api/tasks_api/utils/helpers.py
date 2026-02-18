from datetime import datetime, timedelta, timezone
import calendar

def get_next_run_datetime(recurrence_type: str, recurrence_day_of_week: int = None, recurrence_month_day: int = None) -> datetime | None:
    now = datetime.now(timezone.utc)

    match recurrence_type:
        case "daily":
            next_run = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        case "weekly":
            days_ahead = (recurrence_day_of_week - now.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            next_run = (now + timedelta(days=days_ahead)).replace(hour=0, minute=0, second=0, microsecond=0)
        case "monthly":
            try:
                candidate = datetime(now.year, now.month, recurrence_month_day, tzinfo=timezone.utc)
            except ValueError:
                last_day = calendar.monthrange(now.year, now.month)[1]
                candidate = datetime(now.year, now.month, last_day, tzinfo=timezone.utc)

            if candidate <= now:
                if now.month == 12:
                    next_year = now.year + 1
                    next_month = 1
                else:
                    next_year = now.year
                    next_month = now.month + 1

                try:
                    next_run = datetime(next_year, next_month, recurrence_month_day, tzinfo=timezone.utc)
                except ValueError:
                    last_day = calendar.monthrange(next_year, next_month)[1]
                    next_run = datetime(next_year, next_month, last_day, tzinfo=timezone.utc)
            else:
                next_run = candidate

        case _:
            return None

    return next_run