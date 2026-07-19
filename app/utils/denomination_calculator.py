from decimal import Decimal


class DenominationCalculator:

    @staticmethod
    def calculate(
        balance: Decimal,
        available_denominations: list,
    ) -> list[dict]:

        remaining = int(balance)

        result = []

        denominations = sorted(
            available_denominations,
            key=lambda x: x.denomination,
            reverse=True,
        )

        for denomination in denominations:

            note = denomination.denomination

            available_count = denomination.count

            required = remaining // note

            used = min(
                required,
                available_count,
            )

            if used:

                result.append(
                    {
                        "denomination": note,
                        "count": used,
                    }
                )

            remaining -= note * used

        if remaining != 0:
            raise ValueError(
                "Unable to return exact balance using available denominations."
            )

        return result