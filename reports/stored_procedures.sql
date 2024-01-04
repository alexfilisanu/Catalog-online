CREATE OR REPLACE PROCEDURE get_all_students_above_avg_in_subject
    (IN min_avg integer, IN subject_name varchar(50), OUT no_students integer)
AS $$
BEGIN
    SELECT COUNT(E.ID_elev)
    INTO no_students
    FROM Elevi E
    JOIN Note N ON E.ID_elev = N.ID_elev
    JOIN Materii M ON N.ID_materie = M.ID_materie
    WHERE N.nota >= min_avg AND M.nume = subject_name;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE count_students_without_any_absence
    (OUT no_absence_students INTEGER)
AS $$
BEGIN
    SELECT COUNT(E.ID_Elev)
    INTO no_absence_students
    FROM Elevi E
    LEFT JOIN Absente A ON E.ID_Elev = A.ID_Elev
    WHERE A.ID_Absenta IS NULL OR A.Motivat = TRUE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE get_class_with_most_absences_in_subject
    (IN subject_name VARCHAR(50), OUT class_with_most_absences VARCHAR(20))
AS $$
BEGIN
    SELECT C.Nume
    INTO class_with_most_absences
    FROM Clase C
    JOIN Elevi E ON C.ID_Clasa = E.Clasa
    JOIN Absente A ON E.ID_Elev = A.ID_Elev
    JOIN Materii M ON A.ID_Materie = M.ID_Materie
    WHERE M.Nume = subject_name AND A.Motivat = FALSE
    GROUP BY C.Nume
    ORDER BY COUNT(A.ID_Absenta) DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;
