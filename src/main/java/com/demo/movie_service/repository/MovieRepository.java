package com.demo.movie_service.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.demo.movie_service.repository.entity.Movie;

@Repository
public interface MovieRepository extends JpaRepository<Movie, Integer>{

}