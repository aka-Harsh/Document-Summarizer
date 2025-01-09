package com.demo.movie_service.pojo;

import java.time.LocalDate;

import com.demo.movie_service.repository.entity.Movie;

import jakarta.annotation.Nonnull;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class MoviePojo {
	private int movieId;
	
	@NotNull
	private String movieTitle;
	
	@NotNull
	private String movieLanguage;
	
	@NotNull
	private LocalDate movieReleaseDate;
	
	
	private String movieImageUrl;
}