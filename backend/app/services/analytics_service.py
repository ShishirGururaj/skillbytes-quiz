from pymongo.database import Database


def get_learning_velocity(
    database: Database,
) -> list[dict]:
    pipeline = [
        {
            "$group": {
                "_id": "$user_id",
                "accuracy": {
                    "$avg": {
                        "$cond": [
                            "$is_correct",
                            1,
                            0,
                        ]
                    }
                },
                "avg_response_time": {
                    "$avg": "$response_duration_seconds"
                },
                "response_time_stddev": {
                    "$stdDevPop": "$response_duration_seconds"
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "user_id": "$_id",
                "accuracy": {
                    "$round": [
                        {
                            "$multiply": [
                                "$accuracy",
                                100,
                            ]
                        },
                        2,
                    ]
                },
                "avg_response_time": {
                    "$round": [
                        "$avg_response_time",
                        2,
                    ]
                },
                "consistency_score": {
                    "$round": [
                        {
                            "$multiply": [
                                {
                                    "$max": [
                                        0,
                                        {
                                            "$subtract": [
                                                1,
                                                {
                                                    "$divide": [
                                                        "$response_time_stddev",
                                                        {
                                                            "$max": [
                                                                "$avg_response_time",
                                                                0.001,
                                                            ]
                                                        },
                                                    ]
                                                },
                                            ]
                                        },
                                    ]
                                },
                                100,
                            ]
                        },
                        2,
                    ]
                },
            }
        },
    ]

    rows = list(database.attempts.aggregate(pipeline))

    if not rows:
        return []

    max_response_time = max(
        row["avg_response_time"]
        for row in rows
    )

    min_response_time = min(
        row["avg_response_time"]
        for row in rows
    )

    response_range = max(
        max_response_time - min_response_time,
        0.001,
    )

    results = []

    for row in rows:
        speed_score = (
            (
                max_response_time
                - row["avg_response_time"]
            )
            / response_range
        ) * 100

        learning_velocity = (
            0.50 * row["accuracy"]
            + 0.30 * speed_score
            + 0.20 * row["consistency_score"]
        )

        results.append(
            {
                **row,
                "learning_velocity_index": round(
                    learning_velocity,
                    2,
                ),
            }
        )

    results.sort(
        key=lambda item: item["learning_velocity_index"],
        reverse=True,
    )

    return results


def get_fatigue_analysis(
    database: Database,
    user_id: str,
    quiz_id: str,
) -> list[dict]:
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "quiz_id": quiz_id,
            }
        },
        {
            "$setWindowFields": {
                "partitionBy": {
                    "user_id": "$user_id",
                    "quiz_id": "$quiz_id",
                },
                "sortBy": {
                    "question_shown_at": 1,
                },
                "output": {
                    "question_number": {
                        "$documentNumber": {}
                    }
                },
            }
        },
        {
            "$set": {
                "window_start": {
                    "$multiply": [
                        {
                            "$floor": {
                                "$divide": [
                                    {
                                        "$subtract": [
                                            "$question_number",
                                            1,
                                        ]
                                    },
                                    5,
                                ]
                            }
                        },
                        5,
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$window_start",
                "accuracy": {
                    "$avg": {
                        "$cond": [
                            "$is_correct",
                            1,
                            0,
                        ]
                    }
                },
                "avg_response_time": {
                    "$avg": "$response_duration_seconds"
                },
                "attempts": {
                    "$sum": 1
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "window_start": {
                    "$add": ["$_id", 1]
                },
                "window_end": {
                    "$add": ["$_id", 5]
                },
                "accuracy": {
                    "$round": [
                        {
                            "$multiply": [
                                "$accuracy",
                                100,
                            ]
                        },
                        2,
                    ]
                },
                "avg_response_time": {
                    "$round": [
                        "$avg_response_time",
                        2,
                    ]
                },
                "attempts": 1,
            }
        },
        {
            "$sort": {
                "window_start": 1
            }
        },
    ]

    return list(database.attempts.aggregate(pipeline))


def get_question_difficulty(
    database: Database,
) -> list[dict]:
    pipeline = [
        {
            "$group": {
                "_id": "$question_id",
                "total_attempts": {
                    "$sum": 1
                },
                "accuracy": {
                    "$avg": {
                        "$cond": [
                            "$is_correct",
                            1,
                            0,
                        ]
                    }
                },
                "avg_response_time": {
                    "$avg": "$response_duration_seconds"
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "question_id": "$_id",
                "total_attempts": 1,
                "accuracy_percentage": {
                    "$round": [
                        {
                            "$multiply": [
                                "$accuracy",
                                100,
                            ]
                        },
                        2,
                    ]
                },
                "avg_response_time": {
                    "$round": [
                        "$avg_response_time",
                        2,
                    ]
                },
            }
        },
    ]

    rows = list(database.attempts.aggregate(pipeline))

    if not rows:
        return []

    max_response_time = max(
        row["avg_response_time"]
        for row in rows
    )

    min_response_time = min(
        row["avg_response_time"]
        for row in rows
    )

    response_range = max(
        max_response_time - min_response_time,
        0.001,
    )

    results = []

    for row in rows:
        response_component = (
            (
                row["avg_response_time"]
                - min_response_time
            )
            / response_range
        ) * 100

        accuracy_component = (
            100 - row["accuracy_percentage"]
        )

        difficulty_score = (
            0.70 * accuracy_component
            + 0.30 * response_component
        )

        results.append(
            {
                **row,
                "difficulty_score": round(
                    difficulty_score,
                    2,
                ),
            }
        )

    results.sort(
        key=lambda item: item["difficulty_score"],
        reverse=True,
    )

    return results