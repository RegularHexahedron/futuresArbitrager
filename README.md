# Futures Arbitrage Bot

## Overview

It listens to real-time futures order books, computes implicit interest rates, and detects self-financed arbitrage opportunities across different maturities.

The bot **does not place orders** — it only identifies and reports potential arbitrage situations.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. Configure instruments (optional). utils/instruments.py

3. Set up credentials utils/config.py
4 Run python main.py

## Approach

By means of a WebSocket connection to the MATBA–ROFEX exchange services, it listens to every (best) bid/offer change in the futures of consideration.

Futures and their relevant information are defined in "utils/instruments.py".
They are hardcoded for simplicity, to have full control of a couple of assets.


1. Each time a bid/offer updates, it prints it.
2. Gets BBO for the underlying (actually, it fakes it, just gets the spot price and ignores the bid/ask spread, then overflows the liquidity.)
3. Compute the implicit interest rates. [Implicit Interest Rates](#implicit-interest-rates)
4. Determine arbitrage opportunity. [Arbitrage](#arbitrage)


## Assumptions and Limitations

- The underlying spot price is approximated using a single price (no bid/ask spread).
- Liquidity is assumed to be infinite at the best price.
- Transaction costs, fees, and slippage are ignored.
- No margin requirements or funding constraints are modeled.
- The bot does not execute trades — it only detects opportunities.
- Minimum and maximum trade sizes are not enforced.

## Financial Model

### Implicit Interest Rates

Under the cost of carry model, the price of a future contract $F_{0}$ that matures in $T$ is given by
$$
\begin{equation*}
		F_{0}
	=
		S_{0}
		\exp\left[
			\left(
				r - s + y
			\right)
			T
		\right]
\end{equation*}
$$
where $S_{0}$ is the price of the underlying $r$ is the risk-free interest rate, $s$ the cost of storage (mere possession), and $y$ the yield.

For stocks, $s = 0$. Assuming, the stock does not pay dividend in the period ($y = 0$), we have
$$
\begin{equation*}
		F_{0}
	=
		S_{0}
		e^{rT}
\end{equation*}
$$

By buying (selling) the underlying and buying (selling) the future, we are effectively lending (borrowing) capital. The interest rates at which this is done is implicitly given by the price of the future (and the underlying) by
$$
\begin{equation*}
        r_{\mathrm{lend}}
    =
        \frac{1}{T}
        \ln\left(
            \frac{ 
                F_{0}
            }{
                S_{0}
            }
        \right)
\end{equation*}
$$

If we act as a market taker,
$$
\begin{equation*}
	\left\{
	\begin{alignedat}{2}
			r_{\mathrm{lend}}
		&=
			\frac{1}{T}
			\ln\left(
				\frac{ 
					F_{\mathrm{bid}}
				}{
					S_{\mathrm{ask}}
				}
			\right)
	\\
			r_{\mathrm{borrow}}
		&=
			\frac{1}{T}
			\ln\left(
				\frac{ 
					F_{\mathrm{ask}}
				}{
					S_{\mathrm{bid}}
				}
			\right)
	\end{alignedat}
	\right.
\end{equation*}
$$

### Arbitrage

Arbitraging futures consists on taking both a lender and a borrower position at favorable rates.

For the arbitrage to be fully self-financed, we ask that the amount lent is lesser and returned sooner than the amount borrowed has to be paid.
$$
\begin{equation*}
	\left\{
	\begin{alignedat}{2}
			N_{l}
		&<
			N_{b}
	\\
			T_{l}
		&\leq
			T_{b}
	\end{alignedat}
	\right.
\end{equation*}
$$

Ignoring transaction costs, the PnL of the arbitrage is just the difference between the net interest rate $rt$ times the amount $n$ of the lend and borrow sides. That is
\begin{align*}
		\mathrm{PnL}
	&=
		N_{l}r_{l}T_{l}
	-
		N_{b}r_{b}T_{b}
\\
\intertext{or}
		\mathrm{PnL}
	&=
		N_{l}
		\left(
			r_{l}T_{l}
		-
			r_{n}T_{b}
		\right)
	-
		\Delta N r_{b}T_{b}
\end{align*}
where $\Delta N = N_{b} - N_{l}$.

Since, in the self-funded case, $\Delta N > 0$, we (naturally) require that the lending net interest rate is greater than the net borrowing interest rate.

#### Numeric

We check the conditions sequentially.

First, we check for all pair of futures if 
$$
\begin{equation*}
	\left\{
	\begin{alignedat}{2}
			r_{l}T_{l}
		&<
			r_{b}T_{b}
	\\
			T_{l}
		&\leq
			T_{b}
	\end{alignedat}
	\right.
\end{equation*}
$$


Second, for all possible $N_{l}, N_{b}$ (from the futures and underlying best book orders), we determine the best PnL. If it's positive, it gets defined as an arbitrage opportunity.

It doesn't take into account min/max trade volumes.