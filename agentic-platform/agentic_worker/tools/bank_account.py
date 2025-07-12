from worker.tools.registry import register_tool

def connect_and_get_balance(credentials: str = "") -> str:
    """
    Mock function to simulate connecting to a bank account and retrieving the current balance.
    Args:
        credentials (str, optional): Placeholder for user credentials (not used in mock).
    Returns:
        str: Mocked balance information.
    """
    return "Your current balance is 100 USD."

# Register the tool
register_tool(
    name="connect_and_get_balance",
    func=connect_and_get_balance,
    description="Use this to connect to a mock bank account and retrieve the balance (always returns 100 USD)."
)
