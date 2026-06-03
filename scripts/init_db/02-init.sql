CREATE OR REPLACE FUNCTION func_manage_tag_usage()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        UPDATE tags SET tag_count = tag_count + 1 WHERE id = NEW.tag_id;
    ELSIF (TG_OP = 'DELETE') THEN
        UPDATE tags SET tag_count = tag_count - 1 WHERE id = OLD.tag_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_vacancies_tags_change
AFTER INSERT OR DELETE ON vacancies_tags
FOR EACH ROW
EXECUTE FUNCTION func_manage_tag_usage();
