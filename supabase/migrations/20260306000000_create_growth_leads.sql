-- Monetization / growth lead capture table
-- Stores creator waitlist, newsletter, sponsor, and brand inquiry submissions.

CREATE TABLE IF NOT EXISTS growth_leads (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    lead_type TEXT NOT NULL,
    email TEXT NOT NULL,
    name TEXT,
    company TEXT,
    budget_range TEXT,
    goal TEXT,
    source_page TEXT,
    referrer TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_growth_leads_created_at ON growth_leads(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_growth_leads_type ON growth_leads(lead_type);
CREATE INDEX IF NOT EXISTS idx_growth_leads_email ON growth_leads(email);

CREATE OR REPLACE FUNCTION update_growth_leads_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_growth_leads_updated_at ON growth_leads;
CREATE TRIGGER update_growth_leads_updated_at
    BEFORE UPDATE ON growth_leads
    FOR EACH ROW
    EXECUTE FUNCTION update_growth_leads_updated_at_column();

ALTER TABLE growth_leads ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Anyone can insert growth leads" ON growth_leads;
CREATE POLICY "Anyone can insert growth leads" ON growth_leads
    FOR INSERT
    WITH CHECK (true);

DROP POLICY IF EXISTS "Anyone can read growth leads" ON growth_leads;
CREATE POLICY "Anyone can read growth leads" ON growth_leads
    FOR SELECT
    USING (true);

DROP POLICY IF EXISTS "Anyone can update growth leads" ON growth_leads;
CREATE POLICY "Anyone can update growth leads" ON growth_leads
    FOR UPDATE
    USING (true);
