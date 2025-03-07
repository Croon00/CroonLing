package com.croonling.artistservice.exception;

public class ArtistNotFoundException extends RuntimeException {
  public ArtistNotFoundException(String message) {
    super(message);
  }
}
