import requests
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from config import api_config


@dataclass
class TrainService:
    """Represents a single train service."""
    destination: str
    scheduled_time: str
    expected_time: Optional[str]
    platform: Optional[str]
    status: str  # "On time", "Delayed", "Cancelled", etc.
    operator: Optional[str] = None
    is_cancelled: bool = False
    is_delayed: bool = False


class HuxleyClient:
    """Client for the Huxley JSON API."""

    def __init__(self, base_url: str, access_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.access_token = access_token

    def get_departures(self, station_code: str, num_services: int = 10) -> List[TrainService]:
        """
        Fetch departure board for a given station.

        Args:
            station_code: 3-letter CRS code (e.g., 'PAD' for Paddington)
            num_services: Number of services to retrieve

        Returns:
            List of TrainService objects
        """
        # Build API endpoint
        endpoint = f"{self.base_url}/departures/{station_code}"

        # Add query parameters
        params = {}
        if self.access_token:
            params['accessToken'] = self.access_token
        if num_services:
            params['expand'] = 'true'

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Parse the response
            return self._parse_services(data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching departures: {e}")
            return []
        except (KeyError, ValueError) as e:
            print(f"Error parsing API response: {e}")
            return []

    def _parse_services(self, data: dict) -> List[TrainService]:
        """Parse the Huxley API response into TrainService objects."""
        services = []

        # The response has a 'trainServices' key with the list of services
        train_services = data.get('trainServices', [])

        for service in train_services:
            # Extract destination
            destination_list = service.get('destination', [])
            destination = destination_list[0].get('locationName', 'Unknown') if destination_list else 'Unknown'

            # Extract times
            std = service.get('std', '')  # Scheduled Time of Departure
            etd = service.get('etd', '')  # Estimated Time of Departure

            # Extract platform
            platform = service.get('platform')

            # Determine status
            is_cancelled = service.get('isCancelled', False)
            etd_lower = etd.lower() if etd else ''

            if is_cancelled:
                status = "Cancelled"
                is_delayed = False
            elif etd_lower == "on time":
                status = "On time"
                is_delayed = False
            elif etd_lower == "cancelled":
                status = "Cancelled"
                is_cancelled = True
                is_delayed = False
            elif etd_lower in ["delayed", "no report"]:
                status = "Delayed"
                is_delayed = True
            elif etd and etd != std and etd_lower not in ["on time"]:
                # Time has changed - it's delayed
                status = f"Exp {etd}"
                is_delayed = True
            else:
                status = "On time"
                is_delayed = False

            # Extract operator
            operator = service.get('operator')

            services.append(TrainService(
                destination=destination,
                scheduled_time=std,
                expected_time=etd if etd != std else None,
                platform=platform,
                status=status,
                operator=operator,
                is_cancelled=is_cancelled,
                is_delayed=is_delayed
            ))

        return services


# Create a global client instance
client = HuxleyClient(api_config.BASE_URL, api_config.API_TOKEN)
