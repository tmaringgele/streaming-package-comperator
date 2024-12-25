export type Package = {
    id: number;
    name: string;
    monthly_price_cents: number | null;
    monthly_price_yearly_subscription_in_cents: number | null;
    live: number;
    highlights: number;
};

export type Subscription = {
    package: Package;
    start_date: string;
    yearly: number;
    price: number;
};

export type Game = {
    id: number;
    team_home: string;
    team_away: string;
    starts_at: string;
    covered_by: Package[];
};

export type OptimizationResponse = {
    solver_status: string;
    start_date: string;
    end_date: string;
    cost: number;
    packages: Subscription[];
    games: Game[];
    live_value: number;
    highlight_value: number;
};
