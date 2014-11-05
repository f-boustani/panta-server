from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
	
task_CHOICES =(
	('1','To Do'),
	('2','Doing'),
        ('3','Done'),
)

class Login(models.Model):

    username = models.EmailField()
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    

class Profile(models.Model):
    username = models.ForeignKey(Login)
    projectID = models.IntegerField(max_length=15,null=True)

    class Meta:
        unique_together = ('username','projectID')

    def as_json(self):
            return dict(
                username=self.username,
                name=self.name,
                projectID=self.projectID)



class Projects(models.Model):
    projectID = models.IntegerField(max_length=15)
    projectName = models.CharField(max_length=50)
    manager = models.CharField(max_length=50)
    project_info = models.CharField(max_length=5000)
    progress = models.IntegerField(max_length=15)

    def as_json(self):
            return dict(
                manager=self.manager,
                projectName=self.projectName,
                projectID=self.projectID,
                project_info=self.project_info,
                progress=self.progress)


class Task(models.Model):
    taskID = models.IntegerField(max_length=15)
    task_info = models.CharField(max_length=5000)
    username = models.ForeignKey(Profile)
    deadline = models.DateField(null=True)
    status = models.CharField(max_length=1, choices=task_CHOICES)

    class Meta:
        unique_together = ('taskID','username')

    def as_json(self):
            return dict(
                taskID=self.taskID,
                task_info=self.task_info,
                username=self.username,
                deadline=self.deadline,
                status=self.status)


class User_father(models.Model):
    username = models.ForeignKey(Profile)
    projectID = models.ForeignKey(Projects)
    father = models.CharField(max_length=50)
    semat = models.CharField(max_length=50)
    
    def as_json(self):
            return dict(
                projectID=self.projectID,
                father=self.father,
                username=self.username,
                semat=self.semat)



