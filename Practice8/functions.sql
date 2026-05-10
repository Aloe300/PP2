
CREATE OR REPLACE FUNCTION search_contacts_pattern(pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT * FROM phonebook 
    WHERE phonebook.name ILIKE '%' || pattern || '%' 
       OR phonebook.phone LIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paged(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT * FROM phonebook 
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;