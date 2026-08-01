import streamlit as st


def render_home():
    """
    Renders the interactive rGraph hero section.
    """

    hero_html = """
    <section class="rg-hero">

        <div class="rg-cursor-glow"></div>
        <div class="rg-background-grid"></div>

        <div class="rg-hero-layout">

            <div class="rg-hero-copy">

                <div class="rg-eyebrow">
                    <span class="rg-eyebrow-line"></span>
                    PORTFOLIO RISK & ALLOCATION ENGINE
                </div>

                <div class="rg-wordmark">
                    <span>r</span>Graph
                </div>

                <h1 class="rg-main-title">
                    See the risk behind
                    <span>every allocation.</span>
                </h1>

                <p class="rg-main-description">
                    Analyze historical performance, simulate future outcomes
                    and understand how each allocation changes the risk profile
                    of your portfolio.
                </p>

                <div class="rg-feature-row">

                    <div class="rg-feature-item">
                        <strong>Historical</strong>
                        <span>Returns and drawdowns</span>
                    </div>

                    <div class="rg-feature-item">
                        <strong>Simulation</strong>
                        <span>Parametric and bootstrap</span>
                    </div>

                    <div class="rg-feature-item">
                        <strong>Allocation</strong>
                        <span>Frontier and risk parity</span>
                    </div>

                </div>

            </div>

            <div class="rg-hero-visual" aria-hidden="true">

                <div class="rg-visual-label">
                    <span></span>
                    RISK SCENARIO SURFACE
                </div>

                <svg
                    class="rg-market-map"
                    viewBox="0 0 680 430"
                    preserveAspectRatio="xMidYMid meet"
                >
                    <defs>
                        <linearGradient
                            id="rgLineGradient"
                            x1="0%"
                            y1="0%"
                            x2="100%"
                            y2="0%"
                        >
                            <stop
                                offset="0%"
                                stop-color="#2DD4BF"
                            />

                            <stop
                                offset="55%"
                                stop-color="#35C7FF"
                            />

                            <stop
                                offset="100%"
                                stop-color="#8B5CF6"
                            />
                        </linearGradient>

                        <linearGradient
                            id="rgAreaGradient"
                            x1="0%"
                            y1="0%"
                            x2="0%"
                            y2="100%"
                        >
                            <stop
                                offset="0%"
                                stop-color="#35C7FF"
                                stop-opacity="0.24"
                            />

                            <stop
                                offset="100%"
                                stop-color="#35C7FF"
                                stop-opacity="0"
                            />
                        </linearGradient>

                        <filter id="rgGlow">
                            <feGaussianBlur
                                stdDeviation="5"
                                result="blur"
                            />

                            <feMerge>
                                <feMergeNode in="blur" />
                                <feMergeNode in="SourceGraphic" />
                            </feMerge>
                        </filter>
                    </defs>

                    <g class="rg-chart-grid">
                        <line x1="40" y1="70" x2="650" y2="70" />
                        <line x1="40" y1="145" x2="650" y2="145" />
                        <line x1="40" y1="220" x2="650" y2="220" />
                        <line x1="40" y1="295" x2="650" y2="295" />
                        <line x1="40" y1="370" x2="650" y2="370" />

                        <line x1="110" y1="35" x2="110" y2="390" />
                        <line x1="235" y1="35" x2="235" y2="390" />
                        <line x1="360" y1="35" x2="360" y2="390" />
                        <line x1="485" y1="35" x2="485" y2="390" />
                        <line x1="610" y1="35" x2="610" y2="390" />
                    </g>

                    <path
                        class="rg-chart-area"
                        d="
                            M40,330
                            C95,310 125,345 175,285
                            C220,235 255,275 305,215
                            C355,155 390,205 440,160
                            C490,115 520,145 565,95
                            C600,60 625,75 650,48
                            L650,390
                            L40,390
                            Z
                        "
                    />

                    <path
                        class="rg-chart-line"
                        d="
                            M40,330
                            C95,310 125,345 175,285
                            C220,235 255,275 305,215
                            C355,155 390,205 440,160
                            C490,115 520,145 565,95
                            C600,60 625,75 650,48
                        "
                    />

                    <circle class="rg-node rg-node-one" cx="175" cy="285" r="5" />
                    <circle class="rg-node rg-node-two" cx="305" cy="215" r="5" />
                    <circle class="rg-node rg-node-three" cx="440" cy="160" r="5" />
                    <circle class="rg-node rg-node-four" cx="565" cy="95" r="5" />
                    <circle class="rg-node rg-node-main" cx="650" cy="48" r="7" />
                </svg>

                <div class="rg-visual-footer">
                    Historical data
                    <span></span>
                    Scenario modelling
                    <span></span>
                    Risk optimization
                </div>

            </div>

        </div>

    </section>

    <script>
        (() => {
            const hero = document.querySelector(".rg-hero");

            if (!hero || hero.dataset.cursorBound === "true") {
                return;
            }

            hero.dataset.cursorBound = "true";

            hero.addEventListener("pointermove", (event) => {
                const rect = hero.getBoundingClientRect();

                const x = event.clientX - rect.left;
                const y = event.clientY - rect.top;

                const normalizedX = (x / rect.width) - 0.5;
                const normalizedY = (y / rect.height) - 0.5;

                hero.style.setProperty(
                    "--mouse-x",
                    `${x}px`
                );

                hero.style.setProperty(
                    "--mouse-y",
                    `${y}px`
                );

                hero.style.setProperty(
                    "--shift-x",
                    `${normalizedX * 20}px`
                );

                hero.style.setProperty(
                    "--shift-y",
                    `${normalizedY * 14}px`
                );
            });

            hero.addEventListener("pointerleave", () => {
                hero.style.setProperty("--mouse-x", "72%");
                hero.style.setProperty("--mouse-y", "35%");
                hero.style.setProperty("--shift-x", "0px");
                hero.style.setProperty("--shift-y", "0px");
            });
        })();
    </script>
    """

    st.html(
        hero_html,
        unsafe_allow_javascript=True,
    )