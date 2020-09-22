package com.techday.catvision.daos;

import java.util.Collection;
import java.util.Optional;

public interface Dao<T> {
	 
    Optional<T> get(long id);
    Collection<T> getAll();
    long save(T t);
    void update(T t);
    void delete(T t);
}
