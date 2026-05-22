import pytest

from autocad_mcp_server.security.lisp_policy import LispPolicy
from autocad_mcp_server.utils.errors import PolicyViolation


def test_rejects_shell_primitives() -> None:
    policy = LispPolicy(max_chars=1000, max_depth=10)

    with pytest.raises(PolicyViolation):
        policy.validate('(vl-shell-execute "cmd.exe")')


def test_accepts_simple_expression() -> None:
    policy = LispPolicy(max_chars=1000, max_depth=10)

    validated = policy.validate('(princ "hello")')

    assert validated == '(princ "hello")'
