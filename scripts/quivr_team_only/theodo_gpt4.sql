CREATE OR REPLACE FUNCTION update_max_brains_theodo() RETURNS TRIGGER AS $$
DECLARE
    userEmail TEXT;
    allowedDomains TEXT[] := ARRAY['%@theodo.fr', '%@theodo.com', '%@theodo.co.uk', '%@bam.tech', '%@padok.fr', '%@sicara.com', '%@hokla.com', '%@sipios.com'];
BEGIN
    SELECT email INTO userEmail FROM auth.users WHERE id = NEW.user_id;

    IF userEmail LIKE ANY(allowedDomains) THEN
        -- Ensure the models column is initialized as an array if null
        IF NEW.models IS NULL THEN
            NEW.models := '[]'::jsonb;
        END IF;

        -- Add gpt-4 if not present
        IF NOT NEW.models ? 'gpt-4' THEN
            NEW.models := NEW.models || '["gpt-4"]'::jsonb;
        END IF;

        -- Add gpt-3.5-turbo if not present
        IF NOT NEW.models ? 'gpt-3.5-turbo' THEN
            NEW.models := NEW.models || '["gpt-3.5-turbo"]'::jsonb;
        END IF;

        -- Add gpt-3.5-turbo-16k if not present
        IF NOT NEW.models ? 'gpt-3.5-turbo-16k' THEN
            NEW.models := NEW.models || '["gpt-3.5-turbo-16k"]'::jsonb;
        END IF;

        UPDATE user_settings
        SET 
            max_brains = 30,
            max_brain_size = 100000000,
            daily_chat_credit = 200,
            models = NEW.models
        WHERE user_id = NEW.user_id;
    END IF;

    RETURN NULL;  -- for AFTER triggers, the return value is ignored
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

REVOKE ALL ON FUNCTION update_max_brains_theodo() FROM PUBLIC;

DROP TRIGGER IF EXISTS update_max_brains_theodo_trigger ON user_settings;

CREATE TRIGGER update_max_brains_theodo_trigger 
AFTER INSERT ON user_settings 
FOR EACH ROW 
EXECUTE FUNCTION update_max_brains_theodo();
