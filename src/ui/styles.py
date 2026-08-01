import streamlit as st


def apply_global_styles():
    """
    Applies the global rGraph visual design system.
    """

    st.markdown(
        """
        <style>
        @import url(
            'https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap'
        );
        :root {
            --rg-background: #07111F;
            --rg-sidebar: #091522;
            --rg-surface: #0F1D2E;
            --rg-surface-hover: #13243A;
            --rg-border: #1D3146;
            --rg-border-light: #28435E;
            --rg-primary: #35C7FF;
            --rg-primary-dark: #179FD1;
            --rg-accent: #2DD4BF;
            --rg-text: #EAF2F8;
            --rg-text-muted: #8FA6BA;
            --rg-positive: #34D399;
            --rg-negative: #FB7185;
            --rg-warning: #FBBF24;
        }

        /* =========================
           GLOBAL APP
        ========================= */

        .stApp {
            background:
                radial-gradient(
                    circle at 80% 0%,
                    rgba(53, 199, 255, 0.08),
                    transparent 32%
                ),
                var(--rg-background);
            color: var(--rg-text);
        }

        .block-container {
            max-width: 1440px;
            padding-top: 1.75rem;
            padding-bottom: 4rem;
            padding-left: 2.25rem;
            padding-right: 2.25rem;
        }

        html,
        body,
        .stApp,
        button,
        input,
        textarea,
        select,
        [data-testid="stAppViewContainer"] {
            font-family:
                "Manrope",
                "Segoe UI",
                sans-serif !important;
        }

        h1,
        h2,
        h3 {
            color: var(--rg-text);
            letter-spacing: -0.025em;
        }

        h1 {
            font-size: 2.6rem;
            font-weight: 750;
        }

        h2 {
            font-size: 1.65rem;
            font-weight: 700;
            margin-top: 1.5rem;
        }

        h3 {
            font-size: 1.15rem;
            font-weight: 650;
        }

        p {
            color: #C4D2DE;
            line-height: 1.65;
        }

        hr {
            border-color: var(--rg-border);
        }

        /* =========================
           HEADER
        ========================= */

        [data-testid="stHeader"] {
            background: rgba(7, 17, 31, 0.82);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid rgba(29, 49, 70, 0.65);
        }

        /* =========================
           SIDEBAR
        ========================= */

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #091522 0%,
                    #08121E 100%
                );
            border-right: 1px solid var(--rg-border);
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem;
            padding-left: 1.25rem;
            padding-right: 1.25rem;
        }

        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: var(--rg-text);
        }

        section[data-testid="stSidebar"] label {
            color: #B6C7D6;
            font-size: 0.86rem;
            font-weight: 550;
        }

        /* =========================
           INPUTS
        ========================= */

        [data-baseweb="input"] > div,
        [data-baseweb="select"] > div,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextInput"] input,
        [data-testid="stDateInput"] input {
            background-color: #0D1B2A;
            border-color: var(--rg-border);
            border-radius: 10px;
        }

        [data-baseweb="input"] > div:focus-within,
        [data-baseweb="select"] > div:focus-within {
            border-color: var(--rg-primary);
            box-shadow: 0 0 0 1px var(--rg-primary);
        }

        /* =========================
           BUTTONS
        ========================= */

        .stButton > button {
            min-height: 2.75rem;
            border-radius: 10px;
            border: 1px solid var(--rg-border-light);
            font-weight: 650;
            transition:
                transform 0.18s ease,
                border-color 0.18s ease,
                background-color 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            border-color: var(--rg-primary);
        }

        .stButton > button[kind="primary"] {
            color: #03111D;
            border: none;
            background:
                linear-gradient(
                    135deg,
                    var(--rg-primary),
                    var(--rg-accent)
                );
            box-shadow:
                0 10px 30px rgba(53, 199, 255, 0.18);
        }

        .stButton > button[kind="primary"]:hover {
            color: #03111D;
            box-shadow:
                0 12px 34px rgba(53, 199, 255, 0.28);
        }

        /* =========================
           METRIC CARDS
        ========================= */

        div[data-testid="stMetric"] {
            min-height: 132px;
            padding: 1.25rem 1.3rem;
            background:
                linear-gradient(
                    145deg,
                    rgba(17, 34, 53, 0.96),
                    rgba(12, 26, 42, 0.96)
                );
            border: 1px solid var(--rg-border);
            border-radius: 14px;
            box-shadow:
                0 12px 30px rgba(0, 0, 0, 0.16);
        }

        div[data-testid="stMetric"]:hover {
            border-color: var(--rg-border-light);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--rg-text-muted);
            font-size: 0.82rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.055em;
        }

        div[data-testid="stMetricValue"] {
            color: var(--rg-text);
            font-size: 1.75rem;
            font-weight: 720;
        }

        /* =========================
           TABS
        ========================= */

        div[data-baseweb="tab-list"] {
            gap: 0.45rem;
            margin-bottom: 1.2rem;
            border-bottom: none;
        }

        button[data-baseweb="tab"] {
            min-height: 2.65rem;
            padding-left: 1rem;
            padding-right: 1rem;
            background: var(--rg-surface);
            border: 1px solid var(--rg-border);
            border-radius: 10px;
            color: var(--rg-text-muted);
        }

        button[data-baseweb="tab"]:hover {
            color: var(--rg-text);
            border-color: var(--rg-border-light);
            background: var(--rg-surface-hover);
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--rg-primary);
            border-color: rgba(53, 199, 255, 0.55);
            background: rgba(53, 199, 255, 0.09);
        }

        /* =========================
           DATAFRAMES AND CHARTS
        ========================= */

        div[data-testid="stDataFrame"],
        div[data-testid="stTable"],
        div[data-testid="stVegaLiteChart"] {
            overflow: hidden;
            border: 1px solid var(--rg-border);
            border-radius: 14px;
        }

        /* =========================
           ALERTS AND EXPANDERS
        ========================= */

        div[data-testid="stAlert"] {
            border-radius: 12px;
            border: 1px solid var(--rg-border);
        }

        details {
            background: rgba(15, 29, 46, 0.7);
            border: 1px solid var(--rg-border);
            border-radius: 12px;
        }

        details:hover {
            border-color: var(--rg-border-light);
        }

        /* =========================
           CAPTIONS
        ========================= */

        div[data-testid="stCaptionContainer"] {
            color: var(--rg-text-muted);
        }

        /* =========================
           DOWNLOAD BUTTONS
        ========================= */

        .stDownloadButton > button {
            min-height: 2.75rem;
            border-radius: 10px;
            border: 1px solid var(--rg-border-light);
            background: var(--rg-surface);
            font-weight: 600;
        }

        .stDownloadButton > button:hover {
            color: var(--rg-primary);
            border-color: var(--rg-primary);
            background: var(--rg-surface-hover);
        }

        /* =========================
        HOME HERO
        ========================= */

        .rg-hero {
            --mouse-x: 72%;
            --mouse-y: 35%;
            --shift-x: 0px;
            --shift-y: 0px;

            position: relative;
            min-height: 570px;
            display: flex;
            align-items: center;
            overflow: hidden;
            padding: 4.5rem 0.75rem 4rem;
            margin-bottom: 1.5rem;
            background: transparent;
            border: none;
            box-shadow: none;
        }

        .rg-cursor-glow {
            position: absolute;
            inset: 0;
            z-index: 0;
            pointer-events: none;

            background:
                radial-gradient(
                    520px circle at var(--mouse-x) var(--mouse-y),
                    rgba(53, 199, 255, 0.16),
                    rgba(45, 212, 191, 0.055) 30%,
                    transparent 68%
                );
        }

        .rg-background-grid {
            position: absolute;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            opacity: 0.22;

            background-image:
                linear-gradient(
                    rgba(53, 199, 255, 0.08) 1px,
                    transparent 1px
                ),
                linear-gradient(
                    90deg,
                    rgba(53, 199, 255, 0.08) 1px,
                    transparent 1px
                );

            background-size: 64px 64px;

            mask-image:
                radial-gradient(
                    circle at 72% 42%,
                    black,
                    transparent 69%
                );
        }

        .rg-hero-layout {
            position: relative;
            z-index: 2;
            width: 100%;
            display: grid;
            grid-template-columns:
                minmax(0, 1.05fr)
                minmax(420px, 0.95fr);
            align-items: center;
            gap: 3.5rem;
        }

        .rg-hero-copy {
            max-width: 790px;
        }

        .rg-eyebrow {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.25rem;
            color: #849BAF;
            font-size: 0.69rem;
            font-weight: 700;
            letter-spacing: 0.15em;
        }

        .rg-eyebrow-line {
            width: 32px;
            height: 1px;
            background:
                linear-gradient(
                    90deg,
                    var(--rg-primary),
                    var(--rg-accent)
                );
        }

        .rg-wordmark {
            margin-bottom: 0.8rem;
            color: #EAF2F8;
            font-size: 1.2rem;
            font-weight: 800;
            letter-spacing: -0.045em;
        }

        .rg-wordmark span {
            color: var(--rg-primary);
        }

        .rg-main-title {
            max-width: 810px;
            margin: 0;
            color: #F3F8FC;
            font-size: clamp(3.3rem, 5.8vw, 6rem);
            font-weight: 750;
            line-height: 0.98;
            letter-spacing: -0.065em;
        }

        .rg-main-title span {
            display: block;
            margin-top: 0.15rem;

            background:
                linear-gradient(
                    100deg,
                    #35C7FF,
                    #2DD4BF
                );

            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
        }

        .rg-main-description {
            max-width: 680px;
            margin-top: 1.65rem;
            margin-bottom: 2.2rem;
            color: #9AAFC1;
            font-size: 1.03rem;
            font-weight: 450;
            line-height: 1.75;
        }

        .rg-feature-row {
            display: flex;
            align-items: stretch;
            gap: 0;
            max-width: 760px;
            padding-top: 1.15rem;
            border-top: 1px solid rgba(40, 67, 94, 0.7);
        }

        .rg-feature-item {
            position: relative;
            flex: 1;
            padding-right: 1.5rem;
        }

        .rg-feature-item + .rg-feature-item {
            padding-left: 1.5rem;
            border-left: 1px solid rgba(40, 67, 94, 0.62);
        }

        .rg-feature-item strong {
            display: block;
            margin-bottom: 0.25rem;
            color: #DDE8F1;
            font-size: 0.82rem;
            font-weight: 700;
        }

        .rg-feature-item span {
            display: block;
            color: #71899D;
            font-size: 0.72rem;
            line-height: 1.45;
        }

        .rg-hero-visual {
            position: relative;
            min-height: 450px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transform:
                translate3d(
                    var(--shift-x),
                    var(--shift-y),
                    0
                );
            transition: transform 90ms ease-out;
            will-change: transform;
        }

        .rg-visual-label {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 0.55rem;
            margin-right: 1.5rem;
            color: #6F879B;
            font-size: 0.64rem;
            font-weight: 700;
            letter-spacing: 0.14em;
        }

        .rg-visual-label span {
            width: 6px;
            height: 6px;
            background: var(--rg-accent);
            border-radius: 50%;
            box-shadow:
                0 0 16px rgba(45, 212, 191, 0.8);
        }

        .rg-market-map {
            width: 100%;
            max-height: 430px;
            overflow: visible;
        }

        .rg-chart-grid line {
            stroke: rgba(78, 112, 139, 0.18);
            stroke-width: 1;
        }

        .rg-chart-area {
            fill: url("#rgAreaGradient");
        }

        .rg-chart-line {
            fill: none;
            stroke: url("#rgLineGradient");
            stroke-width: 4;
            stroke-linecap: round;
            filter: url("#rgGlow");
        }

        .rg-node {
            fill: #07111F;
            stroke: #35C7FF;
            stroke-width: 3;
            filter: url("#rgGlow");
        }

        .rg-node-main {
            fill: #35C7FF;
            stroke: #DDF7FF;
            stroke-width: 2;
        }

        .rg-node-one {
            animation: rgPulse 3.2s infinite;
        }

        .rg-node-two {
            animation: rgPulse 3.2s 0.5s infinite;
        }

        .rg-node-three {
            animation: rgPulse 3.2s 1s infinite;
        }

        .rg-node-four {
            animation: rgPulse 3.2s 1.5s infinite;
        }

        .rg-node-main {
            animation: rgPulseMain 2.5s infinite;
        }

        .rg-visual-footer {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 0.65rem;
            margin-right: 1.5rem;
            color: #647C90;
            font-size: 0.63rem;
            letter-spacing: 0.04em;
        }

        .rg-visual-footer span {
            width: 3px;
            height: 3px;
            background: #35C7FF;
            border-radius: 50%;
        }

        @keyframes rgPulse {
            0%,
            100% {
                opacity: 0.55;
            }

            50% {
                opacity: 1;
            }
        }

        @keyframes rgPulseMain {
            0%,
            100% {
                transform: scale(1);
                opacity: 0.85;
            }

            50% {
                transform: scale(1.18);
                opacity: 1;
            }
        }
        
        /* =========================
            PORTFOLIO SETUP
        ========================= */

        .rg-setup {
            position: relative;
            padding: 2.75rem 0 1.5rem;
            margin-top: 0.5rem;
            border-top: 1px solid rgba(40, 67, 94, 0.7);
        }

        .rg-setup-heading {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 2rem;
            margin-bottom: 2rem;
        }

        .rg-section-eyebrow {
            margin-bottom: 0.45rem;
            color: #71899D;
            font-size: 0.66rem;
            font-weight: 700;
            letter-spacing: 0.15em;
        }

        .rg-setup-heading h2 {
            margin: 0;
            color: #EDF5FA;
            font-size: 2rem;
            font-weight: 720;
            letter-spacing: -0.045em;
        }

        .rg-setup-heading p {
            max-width: 600px;
            margin-top: 0.55rem;
            margin-bottom: 0;
            color: #8097AA;
            font-size: 0.9rem;
        }

        .rg-setup-status {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            padding-top: 0.4rem;
            color: #849BAF;
            font-size: 0.65rem;
            font-weight: 750;
            letter-spacing: 0.11em;
        }

        .rg-setup-status span {
            width: 7px;
            height: 7px;
            border-radius: 50%;
        }

        .rg-setup-status.is-valid {
            color: var(--rg-positive);
        }

        .rg-setup-status.is-valid span {
            background: var(--rg-positive);
            box-shadow:
                0 0 12px rgba(52, 211, 153, 0.65);
        }

        .rg-setup-status.is-incomplete {
            color: var(--rg-warning);
        }

        .rg-setup-status.is-incomplete span {
            background: var(--rg-warning);
            box-shadow:
                0 0 12px rgba(251, 191, 36, 0.45);
        }

        .rg-setup-meta {
            display: flex;
            align-items: center;
            gap: 2.5rem;
            margin-bottom: 2rem;
            padding-bottom: 1.4rem;
            border-bottom: 1px solid rgba(40, 67, 94, 0.55);
        }

        .rg-setup-meta-item {
            display: flex;
            align-items: baseline;
            gap: 0.65rem;
        }

        .rg-setup-meta-item span {
            color: #6F879B;
            font-size: 0.72rem;
        }

        .rg-setup-meta-item strong {
            color: #DDE8F1;
            font-size: 0.9rem;
            font-weight: 700;
        }

        .rg-allocation-list {
            display: flex;
            flex-direction: column;
            gap: 0.9rem;
        }

        .rg-allocation-row {
            display: grid;
            grid-template-columns:
                minmax(65px, 90px)
                minmax(120px, 1fr)
                70px;
            align-items: center;
            gap: 1rem;
        }

        .rg-allocation-ticker {
            color: #DDE8F1;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.035em;
        }

        .rg-allocation-track {
            position: relative;
            height: 4px;
            overflow: hidden;
            background: rgba(40, 67, 94, 0.55);
            border-radius: 999px;
        }

        .rg-allocation-fill {
            height: 100%;
            background:
                linear-gradient(
                    90deg,
                    var(--rg-primary),
                    var(--rg-accent)
                );
            border-radius: 999px;
            box-shadow:
                0 0 10px rgba(53, 199, 255, 0.35);
        }

        .rg-allocation-weight {
            color: #9FB3C4;
            font-size: 0.78rem;
            font-weight: 650;
            text-align: right;
        }

        .rg-allocation-empty {
            padding: 1rem 0;
            color: #71899D;
            font-size: 0.82rem;
        }

        .rg-setup-feedback {
            min-height: 2rem;
            margin-top: 1.6rem;
            padding-top: 1.25rem;
            border-top: 1px solid rgba(40, 67, 94, 0.55);
        }

        .rg-setup-issue {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            margin-bottom: 0.45rem;
            color: #E6B86A;
            font-size: 0.76rem;
        }

        .rg-setup-issue span {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 16px;
            height: 16px;
            color: #07111F;
            background: var(--rg-warning);
            border-radius: 50%;
            font-size: 0.62rem;
            font-weight: 800;
        }

        .rg-setup-valid {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            color: #80DDBB;
            font-size: 0.76rem;
        }

        .rg-setup-valid span {
            width: 7px;
            height: 7px;
            background: var(--rg-positive);
            border-radius: 50%;
            box-shadow:
                0 0 10px rgba(52, 211, 153, 0.55);
        }

        /* =========================
            ANALYSIS ACTION
        ========================= */

        .rg-analysis-action-copy {
            max-width: 720px;
            padding-top: 0.45rem;
            color: #71899D;
            font-size: 0.78rem;
            line-height: 1.65;
        }

        .st-key-run_portfolio_analysis {
            display: flex;
            justify-content: flex-end;
        }

        .st-key-run_portfolio_analysis .stButton {
            width: auto;
        }

        .st-key-run_portfolio_analysis .stButton > button {
            position: relative;
            min-height: auto;
            width: auto;
            padding: 0.35rem 0 0.55rem;
            color: var(--rg-primary);
            background: transparent !important;
            border: none !important;
            border-radius: 0;
            box-shadow: none !important;
            font-size: 0.88rem;
            font-weight: 700;
            letter-spacing: -0.01em;
            transition:
                color 180ms ease,
                opacity 180ms ease;
        }

        .st-key-run_portfolio_analysis .stButton > button::after {
            content: "";
            position: absolute;
            right: 0;
            bottom: 0;
            left: 0;
            height: 1px;
            background:
                linear-gradient(
                    90deg,
                    var(--rg-primary),
                    var(--rg-accent)
                );
            transform: scaleX(0.32);
            transform-origin: right;
            transition: transform 220ms ease;
        }

        .st-key-run_portfolio_analysis .stButton > button:hover {
            color: var(--rg-accent);
            background: transparent !important;
            border: none !important;
            transform: none;
        }

        .st-key-run_portfolio_analysis .stButton > button:hover::after {
            transform: scaleX(1);
            transform-origin: left;
        }

        .st-key-run_portfolio_analysis .stButton > button:focus {
            color: var(--rg-primary);
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        .st-key-run_portfolio_analysis .stButton > button:disabled {
            color: #526A7D;
            opacity: 0.55;
            cursor: not-allowed;
        }

        .st-key-run_portfolio_analysis .stButton > button:disabled::after {
            background: #40576A;
            transform: scaleX(0.2);
        }

        /* =========================
            EMPTY DASHBOARD
        ========================= */

        .rg-dashboard-empty {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-top: 1rem;
            padding: 1.15rem 0;
            color: #657E92;
            border-top: 1px solid rgba(40, 67, 94, 0.48);
            font-size: 0.76rem;
            line-height: 1.55;
        }

        .rg-dashboard-empty-line {
            flex: 0 0 auto;
            width: 28px;
            height: 1px;
            background:
                linear-gradient(
                    90deg,
                    var(--rg-primary),
                    transparent
                );
        }
        
        /* =========================
            ANALYSIS COMPLETION
        ========================= */

        .rg-analysis-complete {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            margin: 1.25rem 0 0.75rem;
            padding: 0.85rem 0;
            color: #7F98AC;
            border-top: 1px solid rgba(40, 67, 94, 0.5);
            border-bottom: 1px solid rgba(40, 67, 94, 0.5);
            font-size: 0.75rem;
        }

        .rg-analysis-complete-dot {
            flex: 0 0 auto;
            width: 7px;
            height: 7px;
            background: var(--rg-positive);
            border-radius: 50%;
            box-shadow:
                0 0 12px rgba(52, 211, 153, 0.7);
        }

        .rg-analysis-complete strong {
            color: #8AE2C1;
            font-size: 0.76rem;
            font-weight: 700;
        }

        .rg-analysis-complete strong::after {
            content: "—";
            margin-left: 0.65rem;
            color: #405A70;
        }

        /* =========================
            SIDEBAR STRUCTURE
        ========================= */

        .rg-sidebar-header {
            padding: 0.35rem 0 1.5rem;
            margin-bottom: 0.25rem;
            border-bottom: 1px solid rgba(40, 67, 94, 0.6);
        }

        .rg-sidebar-wordmark {
            color: #EDF5FA;
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.05em;
        }

        .rg-sidebar-wordmark span {
            color: var(--rg-primary);
        }

        .rg-sidebar-subtitle {
            margin-top: 0.2rem;
            color: #607A8F;
            font-size: 0.68rem;
            font-weight: 550;
            letter-spacing: 0.04em;
        }

        .rg-sidebar-section {
            display: flex;
            align-items: flex-start;
            gap: 0.7rem;
            margin-top: 1.6rem;
            margin-bottom: 0.8rem;
        }

        .rg-sidebar-section-number {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 1.55rem;
            height: 1.55rem;
            color: var(--rg-primary);
            border: 1px solid rgba(53, 199, 255, 0.28);
            border-radius: 50%;
            font-size: 0.58rem;
            font-weight: 750;
        }

        .rg-sidebar-section-title {
            color: #DCE8F1;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.025em;
        }

        .rg-sidebar-section-description {
            margin-top: 0.1rem;
            color: #5F778B;
            font-size: 0.62rem;
            line-height: 1.4;
        }

        .rg-assets-column-labels {
            display: grid;
            grid-template-columns:
                0.22fr
                1.15fr
                0.85fr;
            gap: 0.5rem;
            margin-top: 0.85rem;
            margin-bottom: 0.15rem;
            padding: 0 0.1rem;
        }

        .rg-assets-column-labels span {
            color: #5F778B;
            font-size: 0.59rem;
            font-weight: 650;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .rg-assets-column-labels span:last-child {
            text-align: right;
        }

        .rg-sidebar-asset-number {
            padding-top: 0.65rem;
            color: #526B7F;
            font-size: 0.62rem;
            font-weight: 700;
            text-align: center;
        }

        .rg-sidebar-summary {
            margin-top: 1rem;
            padding: 0.9rem 0 0.35rem;
            border-top: 1px solid rgba(40, 67, 94, 0.55);
        }

        .rg-sidebar-summary > div:first-child {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .rg-sidebar-summary span {
            color: #6C8498;
            font-size: 0.67rem;
        }

        .rg-sidebar-summary strong {
            color: #DFEAF2;
            font-size: 0.86rem;
            font-weight: 750;
        }

        .rg-sidebar-allocation-status {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            margin-top: 0.55rem;
            font-size: 0.62rem;
        }

        .rg-sidebar-allocation-status > span {
            width: 6px;
            height: 6px;
            border-radius: 50%;
        }

        .rg-sidebar-allocation-status.is-complete {
            color: #65DCAE;
        }

        .rg-sidebar-allocation-status.is-complete > span {
            background: var(--rg-positive);
            box-shadow:
                0 0 9px rgba(52, 211, 153, 0.55);
        }

        .rg-sidebar-allocation-status.is-incomplete {
            color: #E0AF5A;
        }

        .rg-sidebar-allocation-status.is-incomplete > span {
            background: var(--rg-warning);
            box-shadow:
                0 0 9px rgba(251, 191, 36, 0.4);
        }

        /* Reduce standard Streamlit spacing in sidebar */

        section[data-testid="stSidebar"]
        div[data-testid="stVerticalBlock"] {
            gap: 0.55rem;
        }

        section[data-testid="stSidebar"]
        [data-testid="stTextInput"],
        section[data-testid="stSidebar"]
        [data-testid="stNumberInput"],
        section[data-testid="stSidebar"]
        [data-testid="stDateInput"],
        section[data-testid="stSidebar"]
        [data-testid="stSelectbox"] {
            margin-bottom: 0.1rem;
        }

        section[data-testid="stSidebar"]
        [data-testid="stTextInput"] input,
        section[data-testid="stSidebar"]
        [data-testid="stNumberInput"] input,
        section[data-testid="stSidebar"]
        [data-testid="stDateInput"] input {
            min-height: 2.45rem;
            font-size: 0.78rem;
        }

        section[data-testid="stSidebar"]
        [data-baseweb="select"] > div {
            min-height: 2.45rem;
        }

        /* =========================
            DASHBOARD NAVIGATION
        ========================= */

        .rg-dashboard-navigation-header {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 2rem;
            margin-top: 2.5rem;
            padding-top: 2.5rem;
            border-top: 1px solid rgba(40, 67, 94, 0.58);
        }

        .rg-dashboard-navigation-header span {
            color: #678095;
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 0.15em;
        }

        .rg-dashboard-navigation-header h2 {
            margin-top: 0.35rem;
            margin-bottom: 0;
            color: #EDF5FA;
            font-size: 2rem;
            font-weight: 720;
            letter-spacing: -0.045em;
        }

        .rg-dashboard-navigation-header p {
            max-width: 410px;
            margin: 0 0 0.15rem;
            color: #71899D;
            font-size: 0.78rem;
            text-align: right;
        }


        /* Remove the standard segmented-control container */

        .st-key-dashboard_navigation {
            margin-top: 1.5rem;
            margin-bottom: 2.2rem;
            padding-bottom: 0.15rem;
            border-bottom: 1px solid rgba(40, 67, 94, 0.62);
        }

        .st-key-dashboard_navigation
        [data-testid="stSegmentedControl"] {
            background: transparent;
            border: none;
        }

        .st-key-dashboard_navigation
        [data-testid="stSegmentedControl"] > div {
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            background: transparent;
            border: none;
        }


        /* Individual navigation entries */

        .st-key-dashboard_navigation button {
            position: relative;
            min-height: auto;
            width: auto;
            padding: 0.6rem 0.05rem 0.85rem;
            color: #71899D;
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            font-size: 0.78rem;
            font-weight: 650;
            transition:
                color 160ms ease,
                opacity 160ms ease;
        }

        .st-key-dashboard_navigation button:hover {
            color: #D7E5EF;
            background: transparent !important;
            border: none !important;
            transform: none;
        }

        .st-key-dashboard_navigation button::after {
            content: "";
            position: absolute;
            right: 0;
            bottom: -1px;
            left: 0;
            height: 2px;
            background:
                linear-gradient(
                    90deg,
                    var(--rg-primary),
                    var(--rg-accent)
                );
            transform: scaleX(0);
            transform-origin: center;
            transition: transform 190ms ease;
        }

        .st-key-dashboard_navigation
        button[aria-pressed="true"] {
            color: #EAF2F8;
        }

        .st-key-dashboard_navigation
        button[aria-pressed="true"]::after {
            transform: scaleX(1);
        }

        /* =========================
            OVERVIEW
        ========================= */

        .rg-overview {
            padding-top: 0.5rem;
            padding-bottom: 1.5rem;
        }

        .rg-section-heading {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 2rem;
            margin-bottom: 2rem;
        }

        .rg-section-heading span {
            color: #678095;
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 0.15em;
        }

        .rg-section-heading h2 {
            margin-top: 0.35rem;
            margin-bottom: 0;
            color: #EDF5FA;
            font-size: 2rem;
            font-weight: 720;
            letter-spacing: -0.045em;
        }

        .rg-section-heading p {
            max-width: 430px;
            margin: 0 0 0.15rem;
            color: #71899D;
            font-size: 0.78rem;
            line-height: 1.55;
            text-align: right;
        }


        /* Primary metric strip */

        .rg-overview-primary-metrics {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            padding: 1.5rem 0;
            border-top: 1px solid rgba(40, 67, 94, 0.65);
            border-bottom: 1px solid rgba(40, 67, 94, 0.65);
        }

        .rg-overview-metric {
            display: flex;
            flex-direction: column;
            min-width: 0;
            padding: 0 1.5rem;
        }

        .rg-overview-metric:first-child {
            padding-left: 0;
        }

        .rg-overview-metric + .rg-overview-metric {
            border-left: 1px solid rgba(40, 67, 94, 0.55);
        }

        .rg-overview-metric-label {
            margin-bottom: 0.55rem;
            color: #70889C;
            font-size: 0.64rem;
            font-weight: 700;
            letter-spacing: 0.095em;
            text-transform: uppercase;
        }

        .rg-overview-metric-value {
            overflow: hidden;
            color: #EDF5FA;
            font-size: clamp(1.45rem, 2.2vw, 2rem);
            font-weight: 720;
            letter-spacing: -0.045em;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .rg-overview-metric-value.positive {
            color: #68DDB2;
        }

        .rg-overview-metric-value.negative {
            color: #F18A9A;
        }

        .rg-overview-metric-detail {
            margin-top: 0.4rem;
            color: #5F778B;
            font-size: 0.66rem;
            line-height: 1.4;
        }


        /* Secondary risk metrics */

        .rg-overview-risk-heading {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }

        .rg-overview-risk-heading span {
            flex: 0 0 auto;
            color: #607A8F;
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.14em;
        }

        .rg-overview-risk-heading div {
            width: 100%;
            height: 1px;
            background: rgba(40, 67, 94, 0.5);
        }

        .rg-overview-risk-metrics {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
        }

        .rg-overview-risk-metrics .rg-overview-metric {
            padding-top: 0.4rem;
            padding-bottom: 0.4rem;
        }

        .rg-overview-risk-metrics
        .rg-overview-metric-value {
            font-size: 1.15rem;
        }

        /* =========================
            PERFORMANCE
        ========================= */

        .rg-performance {
            padding-top: 0.5rem;
            padding-bottom: 1.25rem;
        }

        .rg-performance-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            padding: 1.45rem 0;
            border-top: 1px solid rgba(40, 67, 94, 0.65);
            border-bottom: 1px solid rgba(40, 67, 94, 0.65);
        }

        .rg-performance-metric {
            display: flex;
            flex-direction: column;
            min-width: 0;
            padding: 0 1.5rem;
        }

        .rg-performance-metric:first-child {
            padding-left: 0;
        }

        .rg-performance-metric
        + .rg-performance-metric {
            border-left: 1px solid rgba(40, 67, 94, 0.55);
        }

        .rg-performance-metric-label {
            margin-bottom: 0.5rem;
            color: #70889C;
            font-size: 0.64rem;
            font-weight: 700;
            letter-spacing: 0.095em;
            text-transform: uppercase;
        }

        .rg-performance-metric-value {
            color: #EDF5FA;
            font-size: clamp(1.35rem, 2vw, 1.85rem);
            font-weight: 720;
            letter-spacing: -0.045em;
        }

        .rg-performance-metric-value.positive {
            color: #68DDB2;
        }

        .rg-performance-metric-value.negative {
            color: #F18A9A;
        }

        .rg-performance-metric-detail {
            margin-top: 0.35rem;
            color: #5F778B;
            font-size: 0.66rem;
            line-height: 1.4;
        }


        /* Automatic interpretation */

        .rg-performance-reading {
            display: grid;
            grid-template-columns: 170px minmax(0, 1fr);
            gap: 1.5rem;
            margin-top: 1.5rem;
            padding: 1.1rem 0;
            border-bottom: 1px solid rgba(40, 67, 94, 0.48);
        }

        .rg-performance-reading > span {
            padding-top: 0.15rem;
            color: #607A8F;
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.13em;
        }

        .rg-performance-reading p {
            max-width: 850px;
            margin: 0;
            color: #91A6B8;
            font-size: 0.8rem;
            line-height: 1.65;
        }


        /* Chart headings */

        .rg-chart-heading {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 2rem;
            margin-top: 2.4rem;
            margin-bottom: 0.9rem;
        }

        .rg-chart-heading span {
            color: #607A8F;
            font-size: 0.61rem;
            font-weight: 700;
            letter-spacing: 0.14em;
        }

        .rg-chart-heading h3 {
            margin-top: 0.3rem;
            margin-bottom: 0;
            color: #DFEAF2;
            font-size: 1.15rem;
            font-weight: 680;
            letter-spacing: -0.025em;
        }

        .rg-chart-heading p {
            max-width: 430px;
            margin: 0 0 0.1rem;
            color: #657D91;
            font-size: 0.72rem;
            line-height: 1.5;
            text-align: right;
        }
        
        /* =========================
            MONTE CARLO SIMULATION
        ========================= */

        .rg-simulation {
            padding-top: 0.5rem;
            padding-bottom: 1.25rem;
        }

        .rg-simulation-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            padding: 1.45rem 0;
            border-top: 1px solid rgba(40, 67, 94, 0.65);
            border-bottom: 1px solid rgba(40, 67, 94, 0.65);
        }

        .rg-simulation-metric {
            display: flex;
            flex-direction: column;
            min-width: 0;
            padding: 0 1.5rem;
        }

        .rg-simulation-metric:first-child {
            padding-left: 0;
        }

        .rg-simulation-metric
        + .rg-simulation-metric {
            border-left: 1px solid rgba(40, 67, 94, 0.55);
        }

        .rg-simulation-metric-label {
            margin-bottom: 0.5rem;
            color: #70889C;
            font-size: 0.64rem;
            font-weight: 700;
            letter-spacing: 0.095em;
            text-transform: uppercase;
        }

        .rg-simulation-metric-value {
            overflow: hidden;
            color: #EDF5FA;
            font-size: clamp(1.35rem, 2vw, 1.85rem);
            font-weight: 720;
            letter-spacing: -0.045em;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .rg-simulation-metric-value.positive {
            color: #68DDB2;
        }

        .rg-simulation-metric-value.negative {
            color: #F18A9A;
        }

        .rg-simulation-metric-detail {
            margin-top: 0.35rem;
            color: #5F778B;
            font-size: 0.66rem;
            line-height: 1.4;
        }

        .rg-simulation-reading {
            display: grid;
            grid-template-columns: 170px minmax(0, 1fr);
            gap: 1.5rem;
            margin-top: 1.5rem;
            padding: 1.1rem 0;
            border-bottom: 1px solid rgba(40, 67, 94, 0.48);
        }

        .rg-simulation-reading > span {
            padding-top: 0.15rem;
            color: #607A8F;
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.13em;
        }

        .rg-simulation-reading p {
            max-width: 900px;
            margin: 0;
            color: #91A6B8;
            font-size: 0.8rem;
            line-height: 1.65;
        }

        /* =========================
            OPTIMIZATION
        ========================= */

        .rg-optimization {
            padding-top: 0.5rem;
            padding-bottom: 1.25rem;
        }

        .rg-optimization-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            padding: 1.45rem 0;
            border-top: 1px solid rgba(40, 67, 94, 0.65);
            border-bottom: 1px solid rgba(40, 67, 94, 0.65);
        }

        .rg-optimization-metric {
            display: flex;
            flex-direction: column;
            min-width: 0;
            padding: 0 1.5rem;
        }

        .rg-optimization-metric:first-child {
            padding-left: 0;
        }

        .rg-optimization-metric
        + .rg-optimization-metric {
            border-left: 1px solid rgba(40, 67, 94, 0.55);
        }

        .rg-optimization-metric-label {
            margin-bottom: 0.5rem;
            color: #70889C;
            font-size: 0.64rem;
            font-weight: 700;
            letter-spacing: 0.095em;
            text-transform: uppercase;
        }

        .rg-optimization-metric-value {
            overflow: hidden;
            color: #EDF5FA;
            font-size: clamp(1.35rem, 2vw, 1.85rem);
            font-weight: 720;
            letter-spacing: -0.045em;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .rg-optimization-metric-value.positive {
            color: #68DDB2;
        }

        .rg-optimization-metric-value.negative {
            color: #F18A9A;
        }

        .rg-optimization-metric-detail {
            margin-top: 0.35rem;
            color: #5F778B;
            font-size: 0.66rem;
            line-height: 1.4;
        }

        .rg-optimization-reading {
            display: grid;
            grid-template-columns: 170px minmax(0, 1fr);
            gap: 1.5rem;
            margin-top: 1.5rem;
            padding: 1.1rem 0;
            border-bottom: 1px solid rgba(40, 67, 94, 0.48);
        }

        .rg-optimization-reading > span {
            padding-top: 0.15rem;
            color: #607A8F;
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.13em;
        }

        .rg-optimization-reading p {
            max-width: 900px;
            margin: 0;
            color: #91A6B8;
            font-size: 0.8rem;
            line-height: 1.65;
        }
        
        /* =========================
            REBALANCING
        ========================= */

        .rg-rebalancing {
            padding-top: 0.5rem;
            padding-bottom: 1.25rem;
        }

        .rg-rebalancing-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            padding: 1.45rem 0;
            border-top: 1px solid rgba(40, 67, 94, 0.65);
            border-bottom: 1px solid rgba(40, 67, 94, 0.65);
        }

        .rg-rebalancing-metric {
            display: flex;
            flex-direction: column;
            min-width: 0;
            padding: 0 1.5rem;
        }

        .rg-rebalancing-metric:first-child {
            padding-left: 0;
        }

        .rg-rebalancing-metric
        + .rg-rebalancing-metric {
            border-left: 1px solid rgba(40, 67, 94, 0.55);
        }

        .rg-rebalancing-metric-label {
            margin-bottom: 0.5rem;
            color: #70889C;
            font-size: 0.64rem;
            font-weight: 700;
            letter-spacing: 0.095em;
            text-transform: uppercase;
        }

        .rg-rebalancing-metric-value {
            overflow: hidden;
            color: #EDF5FA;
            font-size: clamp(1.35rem, 2vw, 1.85rem);
            font-weight: 720;
            letter-spacing: -0.045em;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .rg-rebalancing-metric-value.positive {
            color: #68DDB2;
        }

        .rg-rebalancing-metric-value.negative {
            color: #F18A9A;
        }

        .rg-rebalancing-metric-detail {
            margin-top: 0.35rem;
            color: #5F778B;
            font-size: 0.66rem;
            line-height: 1.4;
        }

        .rg-rebalancing-reading {
            display: grid;
            grid-template-columns: 170px minmax(0, 1fr);
            gap: 1.5rem;
            margin-top: 1.5rem;
            padding: 1.1rem 0;
            border-bottom: 1px solid rgba(40, 67, 94, 0.48);
        }

        .rg-rebalancing-reading > span {
            padding-top: 0.15rem;
            color: #607A8F;
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.13em;
        }

        .rg-rebalancing-reading p {
            max-width: 900px;
            margin: 0;
            color: #91A6B8;
            font-size: 0.8rem;
            line-height: 1.65;
        }

        /* =========================
            MARKET SENSITIVITY
        ========================= */

        .rg-market {
            padding-top: 0.5rem;
            padding-bottom: 1.25rem;
        }

        .rg-market-strip {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            padding: 1.45rem 0;
            border-top: 1px solid rgba(40, 67, 94, 0.65);
            border-bottom: 1px solid rgba(40, 67, 94, 0.65);
        }

        .rg-market-capture-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            margin-bottom: 1.25rem;
            padding: 1.35rem 0;
            border-top: 1px solid rgba(40, 67, 94, 0.55);
            border-bottom: 1px solid rgba(40, 67, 94, 0.55);
        }

        .rg-market-metric {
            display: flex;
            flex-direction: column;
            min-width: 0;
            padding: 0 1.35rem;
        }

        .rg-market-metric:first-child {
            padding-left: 0;
        }

        .rg-market-metric
        + .rg-market-metric {
            border-left: 1px solid rgba(40, 67, 94, 0.55);
        }

        .rg-market-metric-label {
            margin-bottom: 0.5rem;
            color: #70889C;
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.09em;
            text-transform: uppercase;
        }

        .rg-market-metric-value {
            overflow: hidden;
            color: #EDF5FA;
            font-size: clamp(1.2rem, 1.8vw, 1.7rem);
            font-weight: 720;
            letter-spacing: -0.045em;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .rg-market-metric-value.positive {
            color: #68DDB2;
        }

        .rg-market-metric-value.negative {
            color: #F18A9A;
        }

        .rg-market-metric-detail {
            margin-top: 0.35rem;
            color: #5F778B;
            font-size: 0.64rem;
            line-height: 1.4;
        }

        .rg-market-reading {
            display: grid;
            grid-template-columns: 170px minmax(0, 1fr);
            gap: 1.5rem;
            margin-top: 1.5rem;
            padding: 1.1rem 0;
            border-bottom: 1px solid rgba(40, 67, 94, 0.48);
        }

        .rg-market-reading > span {
            padding-top: 0.15rem;
            color: #607A8F;
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.13em;
        }

        .rg-market-reading p {
            max-width: 900px;
            margin: 0;
            color: #91A6B8;
            font-size: 0.8rem;
            line-height: 1.65;
        }
        
        /* =========================
            DOWNLOADS
        ========================= */

        .rg-downloads {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }

        .rg-download-summary {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            padding: 1.4rem 0;
            border-top: 1px solid rgba(40, 67, 94, 0.65);
            border-bottom: 1px solid rgba(40, 67, 94, 0.65);
        }

        .rg-download-summary > div {
            display: flex;
            flex-direction: column;
            padding: 0 1.5rem;
        }

        .rg-download-summary > div:first-child {
            padding-left: 0;
        }

        .rg-download-summary > div + div {
            border-left: 1px solid rgba(40, 67, 94, 0.55);
        }

        .rg-download-summary span {
            margin-bottom: 0.45rem;
            color: #70889C;
            font-size: 0.63rem;
            font-weight: 700;
            letter-spacing: 0.09em;
            text-transform: uppercase;
        }

        .rg-download-summary strong {
            color: #EDF5FA;
            font-size: 1.35rem;
            font-weight: 720;
            letter-spacing: -0.035em;
        }

        .rg-download-summary strong.positive {
            color: #68DDB2;
        }

        .rg-download-note {
            margin-top: 1.1rem;
            color: #6C8498;
            font-size: 0.72rem;
            line-height: 1.55;
        }


        /* Export categories */

        .rg-download-category {
            display: grid;
            grid-template-columns: auto auto minmax(40px, 1fr);
            align-items: center;
            gap: 0.8rem;
            margin-top: 2.5rem;
            margin-bottom: 0.35rem;
        }

        .rg-download-category-number {
            color: var(--rg-primary);
            font-size: 0.62rem;
            font-weight: 750;
            letter-spacing: 0.08em;
        }

        .rg-download-category h3 {
            margin: 0;
            color: #DDE9F1;
            font-size: 0.88rem;
            font-weight: 680;
        }

        .rg-download-category p {
            margin: 0.12rem 0 0;
            color: #617A8F;
            font-size: 0.64rem;
        }

        .rg-download-category-line {
            height: 1px;
            margin-left: 0.35rem;
            background: rgba(40, 67, 94, 0.5);
        }


        /* Individual export rows */

        [class*="st-key-download_row_"] {
            padding: 1.05rem 0;
            border-bottom: 1px solid rgba(40, 67, 94, 0.42);
        }

        .rg-download-row-title {
            color: #DCE8F1;
            font-size: 0.79rem;
            font-weight: 680;
        }

        .rg-download-row-description {
            max-width: 720px;
            margin-top: 0.22rem;
            color: #71899D;
            font-size: 0.68rem;
            line-height: 1.5;
        }

        .rg-download-row-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem 1rem;
            margin-top: 0.5rem;
        }

        .rg-download-row-meta span {
            position: relative;
            color: #526B7F;
            font-size: 0.58rem;
            font-weight: 650;
            letter-spacing: 0.055em;
            text-transform: uppercase;
        }

        .rg-download-row-meta span + span::before {
            content: "·";
            position: absolute;
            left: -0.62rem;
            color: #365169;
        }


        /* Flat download actions */

        [class*="st-key-download_"]
        .stDownloadButton > button {
            min-height: auto;
            padding: 0.55rem 0.15rem;
            color: #9EDFFF;
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            font-size: 0.69rem;
            font-weight: 700;
        }

        [class*="st-key-download_"]
        .stDownloadButton > button:hover {
            color: #E4F6FF;
            background: transparent !important;
            border: none !important;
            transform: none;
        }

        [class*="st-key-download_"]
        .stDownloadButton > button p {
            font-size: 0.69rem;
        }

        /* =========================
            MONTE CARLO DATA TABLES
        ========================= */

        .rg-mc-table-scroll {
            width: 100%;
            overflow-x: auto;
            margin: 0.35rem 0 1.4rem;
            padding-bottom: 0.25rem;
            scrollbar-width: thin;
            scrollbar-color:
                rgba(73, 111, 140, 0.65)
                transparent;
        }

        .rg-mc-table-scroll::-webkit-scrollbar {
            height: 5px;
        }

        .rg-mc-table-scroll::-webkit-scrollbar-track {
            background: transparent;
        }

        .rg-mc-table-scroll::-webkit-scrollbar-thumb {
            background: rgba(73, 111, 140, 0.65);
            border-radius: 999px;
        }

        .rg-mc-table {
            width: 100%;
            min-width: 900px;
            border-collapse: collapse;
            border-spacing: 0;
            background: transparent;
        }

        .rg-mc-table thead {
            border-top: 1px solid rgba(40, 67, 94, 0.65);
            border-bottom: 1px solid rgba(40, 67, 94, 0.65);
        }

        .rg-mc-table th,
        .rg-mc-table td {
            padding: 0.9rem 1rem;
            text-align: right;
            white-space: nowrap;
        }

        .rg-mc-table thead th {
            color: #667F94;
            font-family:
                "Manrope",
                "Segoe UI",
                sans-serif;
            font-size: 0.59rem;
            font-weight: 700;
            letter-spacing: 0.085em;
            text-transform: uppercase;
        }

        .rg-mc-table thead th:first-child {
            text-align: left;
        }

        .rg-mc-table tbody {
            border-bottom: 1px solid rgba(40, 67, 94, 0.55);
        }

        .rg-mc-table tbody tr {
            border-bottom: 1px solid rgba(40, 67, 94, 0.34);
            transition:
                background 140ms ease;
        }

        .rg-mc-table tbody tr:last-child {
            border-bottom: none;
        }

        .rg-mc-table tbody tr:hover {
            background: rgba(19, 43, 61, 0.3);
        }

        .rg-mc-table tbody th {
            position: sticky;
            left: 0;
            z-index: 1;
            min-width: 185px;
            color: #D8E6EF;
            background: #07111F;
            font-family:
                "Manrope",
                "Segoe UI",
                sans-serif;
            font-size: 0.72rem;
            font-weight: 680;
            text-align: left;
        }

        .rg-mc-table tbody td {
            color: #AFC0CD;
            font-family:
                ui-monospace,
                "SFMono-Regular",
                "Cascadia Code",
                "Roboto Mono",
                Consolas,
                monospace;
            font-size: 0.71rem;
            font-variant-numeric: tabular-nums;
            letter-spacing: -0.015em;
        }

        .rg-mc-table tbody td.is-positive {
            color: #68DDB2;
        }

        .rg-mc-table tbody td.is-warning {
            color: #E9C46A;
        }

        .rg-mc-table tbody td.is-negative {
            color: #F18A9A;
        }

        .rg-mc-table.is-compact th,
        .rg-mc-table.is-compact td {
            padding-top: 0.78rem;
            padding-bottom: 0.78rem;
        }

        /* =========================
            ANALYSIS STATE
        ========================= */

        .rg-analysis-state {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            margin: 1.4rem 0 0.5rem;
            padding: 0.85rem 0;
            border-top: 1px solid rgba(40, 67, 94, 0.52);
            border-bottom: 1px solid rgba(40, 67, 94, 0.52);
            color: #71899D;
            font-size: 0.7rem;
            line-height: 1.5;
        }

        .rg-analysis-state-dot {
            flex: 0 0 auto;
            width: 7px;
            height: 7px;
            border-radius: 50%;
        }

        .rg-analysis-state strong {
            flex: 0 0 auto;
            font-size: 0.69rem;
            font-weight: 720;
            letter-spacing: 0.035em;
        }

        .rg-analysis-state strong::after {
            content: "—";
            margin-left: 0.65rem;
            color: #405B70;
        }

        .rg-analysis-state.is-current
        .rg-analysis-state-dot {
            background: #68DDB2;
            box-shadow:
                0 0 10px rgba(104, 221, 178, 0.55);
        }

        .rg-analysis-state.is-current strong {
            color: #68DDB2;
        }

        .rg-analysis-state.is-stale
        .rg-analysis-state-dot {
            background: #F4C95D;
            box-shadow:
                0 0 10px rgba(244, 201, 93, 0.48);
        }

        .rg-analysis-state.is-stale strong {
            color: #F4C95D;
        }

        /* =========================
           MOBILE
        ========================= */

        @media (max-width: 768px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1rem;
            }

            h1 {
                font-size: 2rem;
            }

            button[data-baseweb="tab"] {
                padding-left: 0.7rem;
                padding-right: 0.7rem;
            }
            .rg-hero {
                min-height: auto;
                padding: 2.5rem 0 3rem;
            }

            .rg-hero-layout {
                grid-template-columns: 1fr;
                gap: 2rem;
            }

            .rg-main-title {
                font-size: 3.1rem;
            }

            .rg-feature-row {
                flex-direction: column;
                gap: 1rem;
            }

            .rg-feature-item {
                padding: 0;
            }

            .rg-feature-item + .rg-feature-item {
                padding-top: 1rem;
                padding-left: 0;
                border-top: 1px solid rgba(40, 67, 94, 0.62);
                border-left: none;
            }

            .rg-hero-visual {
                min-height: 330px;
            }

            .rg-visual-label,
            .rg-visual-footer {
                justify-content: flex-start;
                margin-right: 0;
            }

            .rg-setup-heading {
                flex-direction: column;
                gap: 0.75rem;
            }

            .rg-setup-meta {
                align-items: flex-start;
                flex-direction: column;
                gap: 0.65rem;
            }

            .rg-allocation-row {
                grid-template-columns:
                    65px
                    minmax(80px, 1fr)
                    55px;
                gap: 0.7rem;
            }

            .rg-dashboard-navigation-header {
                align-items: flex-start;
                flex-direction: column;
                gap: 0.75rem;
            }

            .rg-dashboard-navigation-header p {
                text-align: left;
            }

            .st-key-dashboard_navigation
            [data-testid="stSegmentedControl"] > div {
                gap: 0.8rem 1.15rem;
            }

            .st-key-dashboard_navigation button {
                font-size: 0.72rem;
            }

            .rg-section-heading {
                align-items: flex-start;
                flex-direction: column;
                gap: 0.75rem;
            }

            .rg-section-heading p {
                text-align: left;
            }

            .rg-overview-primary-metrics {
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0;
            }

            .rg-overview-primary-metrics
            .rg-overview-metric {
                padding: 1rem;
            }

            .rg-overview-primary-metrics
            .rg-overview-metric:nth-child(odd) {
                padding-left: 0;
                border-left: none;
            }

            .rg-overview-primary-metrics
            .rg-overview-metric:nth-child(n + 3) {
                border-top: 1px solid rgba(40, 67, 94, 0.45);
            }

            .rg-overview-risk-metrics {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .rg-overview-risk-metrics
            .rg-overview-metric {
                padding: 0.9rem;
                border-bottom: 1px solid rgba(40, 67, 94, 0.42);
            }

            .rg-overview-risk-metrics
            .rg-overview-metric:nth-child(odd) {
                padding-left: 0;
                border-left: none;
            }

            .rg-performance-strip {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .rg-performance-metric {
                padding: 1rem;
            }

            .rg-performance-metric:nth-child(odd) {
                padding-left: 0;
                border-left: none;
            }

            .rg-performance-metric:nth-child(n + 3) {
                border-top: 1px solid rgba(40, 67, 94, 0.45);
            }

            .rg-performance-reading {
                grid-template-columns: 1fr;
                gap: 0.55rem;
            }

            .rg-chart-heading {
                align-items: flex-start;
                flex-direction: column;
                gap: 0.55rem;
            }

            .rg-chart-heading p {
                text-align: left;
            }

            .rg-simulation-strip {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .rg-simulation-metric {
                padding: 1rem;
            }

            .rg-simulation-metric:nth-child(odd) {
                padding-left: 0;
                border-left: none;
            }

            .rg-simulation-metric:nth-child(n + 3) {
                border-top: 1px solid rgba(40, 67, 94, 0.45);
            }

            .rg-simulation-reading {
                grid-template-columns: 1fr;
                gap: 0.55rem;
            }

            .rg-optimization-strip {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .rg-optimization-metric {
                padding: 1rem;
            }

            .rg-optimization-metric:nth-child(odd) {
                padding-left: 0;
                border-left: none;
            }

            .rg-optimization-metric:nth-child(n + 3) {
                border-top: 1px solid rgba(40, 67, 94, 0.45);
            }

            .rg-optimization-reading {
                grid-template-columns: 1fr;
                gap: 0.55rem;
            }

            .rg-rebalancing-strip {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .rg-rebalancing-metric {
                padding: 1rem;
            }

            .rg-rebalancing-metric:nth-child(odd) {
                padding-left: 0;
                border-left: none;
            }

            .rg-rebalancing-metric:nth-child(n + 3) {
                border-top: 1px solid rgba(40, 67, 94, 0.45);
            }

            .rg-rebalancing-reading {
                grid-template-columns: 1fr;
                gap: 0.55rem;
            }

            .rg-market-strip,
            .rg-market-capture-strip {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .rg-market-metric {
                padding: 1rem;
            }

            .rg-market-metric:nth-child(odd) {
                padding-left: 0;
                border-left: none;
            }

            .rg-market-metric:nth-child(n + 3) {
                border-top: 1px solid rgba(40, 67, 94, 0.45);
            }

            .rg-market-reading {
                grid-template-columns: 1fr;
                gap: 0.55rem;
            }

            .rg-download-summary {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .rg-download-summary > div {
                padding: 0.9rem;
            }

            .rg-download-summary > div:nth-child(odd) {
                padding-left: 0;
                border-left: none;
            }

            .rg-download-summary > div:nth-child(n + 3) {
                border-top: 1px solid rgba(40, 67, 94, 0.42);
            }

            .rg-download-category {
                grid-template-columns: auto minmax(0, 1fr);
            }

            .rg-download-category-line {
                display: none;
            }

            .rg-download-row-meta {
                gap: 0.4rem 0.9rem;
            }

            .rg-analysis-state {
                align-items: flex-start;
                flex-wrap: wrap;
            }

            .rg-analysis-state strong::after {
                display: none;
            }

            .rg-analysis-state > span:last-child {
                flex-basis: calc(100% - 1.5rem);
                margin-left: 1.35rem;
            }

        }
        </style>
        """,
        unsafe_allow_html=True,
    )