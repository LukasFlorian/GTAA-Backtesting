def init():
    global portfolios
    portfolios = []
    relative_prefix = "📈GTAA-Backtesting/no_database/frontend/"
    def add_prefix(filename: str) -> str:
        return relative_prefix + filename + ".py"