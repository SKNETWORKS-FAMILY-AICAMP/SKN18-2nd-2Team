CREATE TABLE netflixDB.Netflix_customers (
  customer_id              INT PRIMARY KEY AUTO_INCREMENT,
  age                      INT,
  gender                   VARCHAR(10),
  subscription_type        VARCHAR(20),
  region                   VARCHAR(50),
  device                   VARCHAR(50),
  watch_hours              Float,
  last_login_days          INT,
  monthly_fee              Float,
  payment_method           VARCHAR(20),
  number_of_profiles       INT,
  favorite_genre           VARCHAR(30),
  avg_watch_time_per_day   Float,
  churned                  TINYINT(1)
);