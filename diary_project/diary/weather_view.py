from django.http import JsonResponse
from datetime import datetime
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class RandomeWeatherView(LoginRequiredMixin, View):

    TIME_PERIOD_CHOICES = [
        # Ancient Civilizations
        ("ancient_egypt", "Ancient Egypt (3100 BCE - 30 BCE)"),
        ("ancient_rome", "Ancient Rome (753 BCE - 476 CE)"),
        ("ancient_greece", "Ancient Greece (800 BCE - 146 BCE)"),
        ("ancient_china", "Ancient China (2100 BCE - 221 BCE)"),
        # Medieval Period
        ("medieval_europe", "Medieval Europe (476 CE - 1500 CE)"),
        ("medieval_japan", "Medieval Japan (1185 CE - 1603 CE)"),
        ("medieval_arabia", "Islamic Golden Age (750 CE - 1258 CE)"),
        # Modern History
        ("renaissance", "Renaissance (1300 CE - 1700 CE)"),
        ("industrial_revolution", "Industrial Revolution (1760 CE - 1840 CE)"),
        ("modern_age", "Modern Age (1900 CE - Present)"),
        # Near Future
        ("near_future_earth", "Early Space Age Earth (2024-2050)"),
        ("lunar_colonization", "Lunar Colonies Era (2040-2080)"),
        ("solar_system_expansion", "Solar System Expansion (2060-2100)"),
        # Mars Era
        ("early_mars", "Early Mars Settlement (2100-2130)"),
        ("mars_terraform", "Mars Terraforming Period (2130-2170)"),
        ("established_mars", "Established Mars Civilization (2170-2200)"),
        # Solar System Era
        ("asteroid_mining", "Asteroid Belt Colonization (2200-2300)"),
        ("gas_giant_stations", "Gas Giant Stations Era (2300-2400)"),
        ("kuiper_outposts", "Kuiper Belt Outposts (2400-2500)"),
        # Interstellar Era
        ("proxima_colonization", "Proxima Centauri Colony (2500-2600)"),
        ("stellar_expansion", "Multi-Star Expansion (2600-2800)"),
        ("galactic_pioneers", "Early Galactic Age (2800-3000)"),
        # Far Future Eras
        ("galactic_civilization", "Galactic Civilization (3000-5000)"),
        ("interstellar_empire", "Interstellar Empire (5000-10000)"),
        ("cosmic_age", "Cosmic Civilization (10000+)"),
        # Alternative Future Paths
        ("post_singularity", "Post-Singularity Era"),
        ("digital_consciousness", "Digital Consciousness Age"),
        ("bio_synthetic_fusion", "Bio-Synthetic Fusion Era"),
        ("quantum_realm", "Quantum Realm Civilization"),
        ("parallel_worlds", "Multi-Dimensional Society"),
    ]

    def get_weather_conditions(self, time_period, location):
        # Base weather parameters
        weather_data = {
            "temperature": 0,
            "humidity": 0,
            "pressure": 0,
            "weather_description": random.choice(
                [
                    "Scorching desert heat",
                    "Nile River floods",
                    "Khamaseen wind storms",
                    "Clear skies",
                ]
            ),
            "additional_effects": [],
            "measurement_system": "metric",
            "data_reliability": "historical approximation",
        }

        # Ancient civilizations weather patterns
        if time_period.startswith("ancient_"):
            if time_period == "ancient_egypt":
                weather_data.update(
                    {
                        "temperature": random.uniform(25, 45),
                        "humidity": random.uniform(10, 30),
                        "weather_description": random.choice(
                            [
                                "Scorching desert heat",
                                "Nile River floods",
                                "Khamaseen wind storms",
                                "Clear skies",
                            ]
                        ),
                    }
                )
            elif time_period == "ancient_rome":
                weather_data.update(
                    {
                        "temperature": random.uniform(10, 35),
                        "humidity": random.uniform(40, 70),
                        "weather_description": random.choice(
                            [
                                "Mediterranean sunshine",
                                "Spring rains",
                                "Mild winter frost",
                                "Summer heat",
                            ]
                        ),
                    }
                )

        # Future scenarios
        elif time_period.startswith("near_future"):
            weather_data.update(
                {
                    "temperature": random.uniform(15, 40),
                    "humidity": random.uniform(30, 80),
                    "weather_description": random.choice(
                        [
                            "Regulated climate dome conditions",
                            "Engineered weather patterns",
                            "Carbon capture cooling effect",
                            "Weather control system active",
                        ]
                    ),
                    "additional_effects": [
                        "Solar radiation warnings",
                        "Air quality monitoring",
                    ],
                }
            )

        # Mars colonies
        elif "mars" in time_period:
            weather_data.update(
                {
                    "temperature": random.uniform(-80, 20),
                    "pressure": random.uniform(
                        600, 750
                    ),  # Assuming partial terraforming
                    "weather_description": random.choice(
                        [
                            "Dust storm approaching",
                            "Clear Martian skies",
                            "Terraformed atmosphere conditions",
                            "Polar ice cap variations",
                        ]
                    ),
                    "additional_effects": ["Radiation levels", "Dust particle density"],
                }
            )

        # Space stations and outposts
        elif any(
            era in time_period for era in ["lunar", "asteroid", "gas_giant", "kuiper"]
        ):
            weather_data.update(
                {
                    "temperature": "Regulated: " + str(random.uniform(18, 25)),
                    "pressure": "Artificial: 1 atm",
                    "weather_description": "Controlled environment",
                    "additional_effects": [
                        "Artificial gravity",
                        "Radiation shielding status",
                    ],
                }
            )

        # Far future and alternative paths
        elif any(
            era in time_period
            for era in ["quantum", "digital", "bio_synthetic", "parallel"]
        ):
            weather_data.update(
                {
                    "weather_description": "Non-standard environmental conditions",
                    "additional_effects": [
                        "Quantum fluctuations",
                        "Reality distortions",
                    ],
                    "measurement_system": "advanced metrics",
                }
            )

        # Add location-specific modifications
        if location:
            weather_data["location_details"] = {
                "name": location,
                "local_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "coordinates": f"Sample coordinates for {location}",
            }

        return weather_data

    def get(self, request):
        time_period = request.GET.get("time_period")
        location = request.GET.get("location")

        # Validate time period
        valid_periods = [choice[0] for choice in self.TIME_PERIOD_CHOICES]
        if not time_period or time_period not in valid_periods:
            return JsonResponse(
                {
                    "error": "Invalid or missing time period",
                    "valid_periods": valid_periods,
                },
                status=400,
            )

        # Validate location
        if not location:
            return JsonResponse({"error": "Location is required"}, status=400)

        # Generate weather data
        weather_data = self.get_weather_conditions(time_period, location)

        return JsonResponse(
            {
                "time_period": time_period,
                "location": location,
                "weather_data": weather_data,
                "generated_at": datetime.now().isoformat(),
            }
        )
