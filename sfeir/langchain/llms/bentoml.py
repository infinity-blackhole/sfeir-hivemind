"""Wrapper around bentoml APIs."""

import logging
from typing import Any, Dict, List, Optional

import bentoml
from langchain.callbacks.manager import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain.llms.base import LLM
from pydantic import Extra, PrivateAttr

logger = logging.getLogger(__name__)


class BentoML(LLM):
    """Wrapper for accessing bentoml.

    To use, you should have the bentoml library installed:

    .. code-block:: bash

        pip install bentoml

    Learn more at: https://github.com/bentoml/bentoml

    Example running an LLM model locally managed by bentoml:
        .. code-block:: python

            from langchain.llms import bentoml
            llm = BentoML(model_tag='flan-t5')
            llm("What is the difference between a duck and a goose?")

    For all available supported models, you can run 'bentoml models'.

    If you have a bentoml server running, you can also use it remotely:
        .. code-block:: python

            from langchain.llms import bentoml
            llm = bentoml(server_url='http://localhost:3000')
            llm("What is the difference between a duck and a goose?")
    """

    model_tag: str
    """Initialize this LLM instance in current process by default. Should
    only set to False when using in conjunction with BentoML Service."""
    llm_kwargs: Dict[str, Any]
    """Key word arguments to be passed to bentoml.LLM"""

    _runner: bentoml.Runner = PrivateAttr(default=None)

    class Config:
        extra = Extra.forbid

    def __init__(
        self,
        model_tag: str,
        **llm_kwargs: Any,
    ):
        try:
            import bentoml
        except ImportError as e:
            raise ImportError(
                "Could not import bentoml. Make sure to install it with "
                "'pip install bentoml.'"
            ) from e

        llm_kwargs = llm_kwargs or {}

        # since the LLM are relatively huge, we don't actually want to convert the
        # Runner with embedded when running the server. Instead, we will only set
        # the init_local here so that LangChain users can still use the LLM
        # in-process. Wrt to BentoML users, setting embedded=False is the expected
        # behaviour to invoke the runners remotely
        self._runner = bentoml.transformers.get(model_tag).to_runner()
        super().__init__(
            **{
                "model_tag": model_tag,
                "llm_kwargs": llm_kwargs,
            }
        )

    @property
    def runner(self) -> bentoml.Runner:
        """
        Get the underlying bentoml.Runner instance for integration with BentoML.

        Example:
        .. code-block:: python

            llm = BentoML(model_tag='flan-t5')
            tools = load_tools(["serpapi", "llm-math"], llm=llm)
            agent = initialize_agent(
                tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
            )
            svc = bentoml.Service("langchain-bentoml", runners=[llm.runner])

            @svc.api(input=Text(), output=Text())
            def chat(input_text: str):
                return agent.run(input_text)
        """
        if self._runner is None:
            raise ValueError("bentoml must be initialized locally with 'model_name'")
        return self._runner

    @property
    def _llm_type(self) -> str:
        return "bentoml"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        return self._runner.generate.run(prompt, **kwargs)

    async def _acall(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        return await self._runner.generate.async_run(prompt, **kwargs)
