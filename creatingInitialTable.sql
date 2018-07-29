CREATE TABLE calorieCounter (
    identification int NOT NULL AUTO_INCREMENT,
    trackDate date NOT NULL UNIQUE,
    calories int,
    carbs int,
    protein int,
    fat int,
    weight float,
    PRIMARY KEY(identification)
);

Insert into calorieCounter (trackDate, calories, carbs, protein, fat, weight) Values ('2018-07-11', 1500, 20, 40, 60, 140.1);
Insert into calorieCounter (trackDate, calories, carbs, protein, fat, weight) Values (sysdate(), 1700, 30, 50, 20, 135.1);

select sysdate()

alter table calorieCounter rename column carbohydrates to carbs;

select * from calorieCounter;

delete from calorieCounter;

drop table calorieCounter;