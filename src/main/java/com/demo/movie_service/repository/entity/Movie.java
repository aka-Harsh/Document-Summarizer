package com.demo.movie_service.repository.entity;

import java.time.LocalDate;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data

@Entity
@Table(name="movie_details")
public class Movie {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name="movie_id")
	private int movieId;
	
	@Column(name="movie_title")
	private String movieTitle;
	
	@Column(name="movie_language")
	private String movieLanguage;
	
	@Column(name="movie_release_date")
	private LocalDate movieReleaseDate;
	
	@Column(name="movie_image_url")
	private String movieImageUrl;
}