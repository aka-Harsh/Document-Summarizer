package com.demo.movie_service.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.demo.movie_service.pojo.MoviePojo;
import com.demo.movie_service.service.MovieService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api")
public class MovieController {

	@Autowired
	MovieService movieService;

	@GetMapping("/movies")
	public ResponseEntity<List<MoviePojo>> getAllMovies() {
		return new ResponseEntity<List<MoviePojo>>(movieService.getAllMovies(), HttpStatus.OK);
	}

	@GetMapping("/movies/{mid}")
	public ResponseEntity<MoviePojo> getAMovie(@PathVariable("mid") int movieId) {
		return new ResponseEntity<MoviePojo>(movieService.getAMovie(movieId), HttpStatus.OK);
	}

	@PostMapping("/movies")
	public ResponseEntity<MoviePojo> addMovie(@RequestBody @Valid MoviePojo moviePojo) {
		return new ResponseEntity<MoviePojo>(movieService.addMovie(moviePojo), HttpStatus.OK);
	}

	@PutMapping("/movies")
	public ResponseEntity<MoviePojo> updateMovie(@RequestBody @Valid MoviePojo moviePojo) {
		return new ResponseEntity<MoviePojo>(movieService.updateMovie(moviePojo), HttpStatus.OK);
	}

	@DeleteMapping("/movies/{mid}")
	public ResponseEntity<Void> deleteMovie(@PathVariable("mid") int movieId) {
		movieService.deleteMovie(movieId);
		return new ResponseEntity<Void>(HttpStatus.OK);
	}
}