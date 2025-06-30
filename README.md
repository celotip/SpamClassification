# Report Spam

## Background

This web app classify spam on comments based on calculated ML (Machine Learning) prediction, and manually classify them as spam if reported more than 3 (three) times.

## API Endpoints

1. `api/feed/ [name='api_feed']`
2. `api/create/ [name='api_create_post']`
3. `api/delete/<int:post_id>/ [name='api_delete_post']`
4. `posts/<int:post_id>/comments/ [name='api_post_comments']`
5. `posts/<int:post_id>/comments/create/ [name='api_create_comment']`
6. `comments/<int:comment_id>/report/ [name='api_report_comment']`
7. `comments/<int:comment_id>/delete/ [name='api_comment_delete']`
8. `api/evaluate/ [name='api_evaluate_accuracy']`
9. `api-token-auth/ [name='api_token_auth']`

## Macine Learning Training & Dataset

Dataset was used from spam.csv, which can be downloaded here
https://drive.google.com/file/d/1JhO_MmioM7BsQl_peU5VCB5CWl7z-dN8/view?usp=share_link

The dataset was trained using `TfidfVectorizer`as vectorizer and `LogisticRegression` model.

Everytime new reported comment is classified as spam, the model is retrained using new data, and dataset is updated locally. Example of screenshot taken after two separate comments were marked as spam

https://drive.google.com/file/d/1Q3fIQGBoJJPUobWuzOayMm7uI04oTKCS/view?usp=share_link

https://drive.google.com/file/d/1YmH8gEa07ratCl-ZlsjUAFhEedOsmZaH/view?usp=share_link

## Login Credentials

- `ghifari`
- `marcel`
- `user3`
- `user4`

password : `asdf`
