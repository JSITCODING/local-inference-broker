import pytest

from local_inference_broker.models import ProviderName, RunRequest, TaskName
from local_inference_broker.providers.deterministic import DeterministicProvider


@pytest.mark.parametrize(
    ("task", "input_text", "expected_output"),
    [
        (TaskName.ASK, "  synthetic   request  ", "synthetic request"),
        (
            TaskName.SUMMARIZE,
            "First synthetic fact. Second synthetic fact. Third synthetic fact.",
            "First synthetic fact. Second synthetic fact.",
        ),
    ],
)
@pytest.mark.asyncio
async def test_plain_text_tasks_are_predictable(
    task: TaskName,
    input_text: str,
    expected_output: str,
) -> None:
    result = await DeterministicProvider().run(
        RunRequest(task=task, input=input_text, provider=ProviderName.DETERMINISTIC)
    )
    assert result.output == expected_output
    assert result.provider == "deterministic"
    assert result.warnings


@pytest.mark.asyncio
async def test_extract_returns_at_most_twenty_structured_items() -> None:
    items = [f"synthetic-item-{index}" for index in range(25)]
    result = await DeterministicProvider().run(
        RunRequest(
            task=TaskName.EXTRACT,
            input="\n".join(items),
            provider=ProviderName.DETERMINISTIC,
        )
    )
    assert result.structured == {"items": items[:20]}
    assert result.output.splitlines() == items[:20]
