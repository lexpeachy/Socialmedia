# Social Media API
http://127.0.0.1:8000/api
A RESTful API built with Django and Django REST Framework, enabling users to create posts, follow other users, and view a personalized feed.


## Overview

This project is a backend API for a social media platform. It allows users to:
- Create, update, and delete posts.
- Follow and unfollow other users.
- View a feed of posts from followed users.

## Features

- **Post Management**: Users can create, update, delete, and view posts.
- **User Profiles**: Each user has a bio and profile picture.
- **Follow System**: Users can follow/unfollow others.
- **Feed**: View posts from followed users in reverse chronological order.
- **Authentication**: Secure login with JWT-based authentication.

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (via `rest_framework_simplejwt`)
- **Database**:  MySQL
- **Hosting**: python anywhere

## **API Endpoints**
```markdown
## API Endpoints

### Authentication
- `POST /api/token/`: Obtain JWT access and refresh tokens.
- `POST /api/token/refresh/`: Refresh access token.

### Users
- `GET /api/users/`: List all users.
- `POST /api/users/`: Create a new user.
- `GET /api/users/<id>/`: Retrieve a user.

### Posts
- `GET /api/posts/`: List all posts.
- `POST /api/posts/`: Create a post.
- `PUT /api/posts/<id>/`: Update a post.
- `DELETE /api/posts/<id>/`: Delete a post.

### Followers
- `POST /api/followers/`: Follow a user.
- `DELETE /api/followers/unfollow/<user_id>/`: Unfollow a user.

### Feed
- `GET /api/feed/`: View feed of posts from followed users.


