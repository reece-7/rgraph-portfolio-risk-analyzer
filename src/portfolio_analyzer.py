import pandas as pd

from src.data_loader import (
    download_price_data,
    calculate_daily_returns,
    validate_weights
)

from src.risk_metrics import (
    calculate_portfolio_returns,
    calculate_cumulative_values,
    calculate_performance_summary
)

from src.monte_carlo import (
    run_parametric_monte_carlo,
    run_bootstrap_monte_carlo,
    calculate_simulation_risk_metrics
)

from src.portfolio_optimization import (
    generate_random_portfolios,
    identify_optimal_portfolios,
    calculate_risk_parity_weights
)

from src.rebalancing import (
    compare_rebalancing_strategies,
    compare_transaction_cost_rebalancing
)

from src.market_sensitivity import (
    calculate_market_sensitivity_summary,
    calculate_capture_summary,
    calculate_rolling_beta
)


def analyze_portfolio(
    tickers,
    weights,
    start_date="2018-01-01",
    end_date=None,
    initial_value=10_000,
    n_simulations=10_000,
    time_horizon=252,
    simulation_end_date=None,
    trading_days=252,
    risk_free_rate=0.00,
    benchmark_ticker="SPY",
    transaction_cost_rates=None,
    random_seed=42,
    progress_callback=None,
):
    """
    Runs the full portfolio analysis pipeline.

    This is the main engine of the final project.
    """

    def report_progress(label):
        """
        Sends a progress update when a callback
        has been provided by the interface.
        """

        if progress_callback is not None:
            progress_callback(label)

    # Make sure the benchmark is included in downloaded data
    all_tickers = list(dict.fromkeys(list(tickers) + [benchmark_ticker]))

    report_progress(
        "Downloading and validating market data"
    )

    # Download price data
    prices = download_price_data(
        tickers=all_tickers,
        start_date=start_date,
        end_date=end_date
    )

    historical_start_date = (
        pd.Timestamp(prices.index[0])
        .normalize()
    )

    historical_end_date = (
        pd.Timestamp(prices.index[-1])
        .normalize()
    )

    simulation_start_date = historical_end_date

    resolved_simulation_end_date = None


    if simulation_end_date is not None:
        resolved_simulation_end_date = (
            pd.Timestamp(simulation_end_date)
            .normalize()
        )

        if (
            resolved_simulation_end_date
            <= simulation_start_date
        ):
            raise ValueError(
                "Simulation end date must be later than "
                "the final available historical market date."
            )

        if trading_days == 365:
            time_horizon = (
                resolved_simulation_end_date
                - simulation_start_date
            ).days

        else:
            simulated_dates = pd.bdate_range(
                start=(
                    simulation_start_date
                    + pd.Timedelta(days=1)
                ),
                end=resolved_simulation_end_date,
            )

            time_horizon = len(simulated_dates)

        if time_horizon < 21:
            raise ValueError(
                "The selected simulation period must contain "
                "at least 21 simulated periods."
            )

    report_progress(
        "Building historical portfolio analytics"
    )

    # Calculate daily returns
    returns = calculate_daily_returns(prices)

    # Keep only portfolio assets for portfolio calculations
    portfolio_returns_data = returns[tickers]

    # Validate and align portfolio weights
    weights = validate_weights(
        weights=weights,
        expected_assets=portfolio_returns_data.columns
    )

    # Historical portfolio returns and values
    portfolio_returns = calculate_portfolio_returns(
        returns=portfolio_returns_data,
        weights=weights
    )

    portfolio_values = calculate_cumulative_values(
        portfolio_returns=portfolio_returns,
        initial_value=initial_value
    )

    performance_summary = calculate_performance_summary(
        portfolio_returns=portfolio_returns,
        initial_value=initial_value,
        trading_days=trading_days,
        risk_free_rate=risk_free_rate
    )

    report_progress(
        "Running parametric Monte Carlo scenarios"
    )

    # Parametric Monte Carlo
    parametric_paths, parametric_final_values = run_parametric_monte_carlo(
        returns=portfolio_returns_data,
        weights=weights,
        initial_value=initial_value,
        n_simulations=n_simulations,
        time_horizon=time_horizon,
        random_seed=random_seed
    )

    parametric_metrics = calculate_simulation_risk_metrics(
        final_values=parametric_final_values,
        initial_value=initial_value
    )

    report_progress(
        "Running bootstrap Monte Carlo scenarios"
    )

    # Bootstrap Monte Carlo
    bootstrap_paths, bootstrap_final_values = run_bootstrap_monte_carlo(
        returns=portfolio_returns_data,
        weights=weights,
        initial_value=initial_value,
        n_simulations=n_simulations,
        time_horizon=time_horizon,
        random_seed=random_seed
    )

    bootstrap_metrics = calculate_simulation_risk_metrics(
        final_values=bootstrap_final_values,
        initial_value=initial_value
    )

    monte_carlo_comparison = pd.DataFrame({
        "Parametric Monte Carlo": parametric_metrics,
        "Bootstrap Monte Carlo": bootstrap_metrics
    }).T

    report_progress(
        "Optimizing portfolio allocation"
    )

    # Efficient Frontier
    efficient_frontier = generate_random_portfolios(
        returns=portfolio_returns_data,
        n_portfolios=5_000,
        trading_days=trading_days,
        risk_free_rate=risk_free_rate,
        random_seed=random_seed
    )

    optimal_portfolios = identify_optimal_portfolios(
        efficient_frontier
    )

    # Risk Parity
    risk_parity_weights = calculate_risk_parity_weights(
        returns=portfolio_returns_data,
        trading_days=trading_days
    )

    report_progress(
        "Evaluating rebalancing strategies and costs"
    )

    # Rebalancing analysis
    custom_portfolio = {
        "Custom Portfolio": weights.to_dict()
    }

    rebalancing_summary, rebalancing_paths = compare_rebalancing_strategies(
        returns=portfolio_returns_data,
        portfolios=custom_portfolio,
        initial_value=initial_value,
        trading_days=trading_days,
        risk_free_rate=risk_free_rate
    )

    # Transaction cost rebalancing analysis
    transaction_cost_summary, transaction_cost_paths = compare_transaction_cost_rebalancing(
        returns=portfolio_returns_data,
        portfolios=custom_portfolio,
        initial_value=initial_value,
        trading_days=trading_days,
        risk_free_rate=risk_free_rate,
        transaction_cost_rates=transaction_cost_rates
    )

    report_progress(
        "Measuring benchmark sensitivity"
    )

    # Market sensitivity analysis
    benchmark_returns = returns[benchmark_ticker]

    market_sensitivity_summary = calculate_market_sensitivity_summary(
        portfolio_returns=portfolio_returns,
        benchmark_returns=benchmark_returns,
        trading_days=trading_days
    )

    capture_summary = calculate_capture_summary(
        portfolio_returns=portfolio_returns,
        benchmark_returns=benchmark_returns
    )

    rolling_beta = calculate_rolling_beta(
        portfolio_returns=portfolio_returns,
        benchmark_returns=benchmark_returns
    )

    report_progress(
        "Finalizing dashboard results"
    )

    results = {
        "historical_start_date": historical_start_date,
        "historical_end_date": historical_end_date,
        "simulation_start_date": simulation_start_date,
        "simulation_end_date": resolved_simulation_end_date,
        "time_horizon": int(time_horizon),
        "prices": prices,
        "returns": returns,
        "portfolio_returns": portfolio_returns,
        "portfolio_values": portfolio_values,
        "performance_summary": performance_summary,
        "parametric_paths": parametric_paths,
        "parametric_final_values": parametric_final_values,
        "bootstrap_paths": bootstrap_paths,
        "bootstrap_final_values": bootstrap_final_values,
        "monte_carlo_comparison": monte_carlo_comparison,
        "efficient_frontier": efficient_frontier,
        "optimal_portfolios": optimal_portfolios,
        "risk_parity_weights": risk_parity_weights,
        "rebalancing_summary": rebalancing_summary,
        "rebalancing_paths": rebalancing_paths,
        "transaction_cost_summary": transaction_cost_summary,
        "transaction_cost_paths": transaction_cost_paths,
        "market_sensitivity_summary": market_sensitivity_summary,
        "capture_summary": capture_summary,
        "rolling_beta": rolling_beta
    }

    return results