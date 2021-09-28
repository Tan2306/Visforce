# Visforce
Visforce

General Description: 
VisForce is an employee interface for a small business enterprise named ******, which is based in Delhi. ***** is a brand specialising in leather products like belts, wallets, etc., largely selling on Amazon, Flipkart, and their own website. The company required an employee interface website to cater to its small workforce (about 20-30 people), whose major requirements are outlined below. 
Visforce is designed to help employees manage and access company data in an efficient manner. We focus on the databases provided by them, specifically, their target audiences, supplier information, and past sales. 

Major Requirements: There will be two types of users in our software. The Employees and the Admin. They would have a varying set of use cases as discussed below.

An employee should be able to -
Login with the login credentials given to them by the company.
Access/filter a collection of company-given databases that we call ‘VisDatabases’. It includes:
Target Audience records (>1000 records)
Past sales records (>300 records)
Supplier contact information (~20 records)
Give anonymous feedback about concerns with the management or any other such complaints.
Apply for leave and receive its status (i.e. awaiting decision/granted/rejected).
See announcements made by the company administration.

An admin should be able to -
Login to the interface.
Upload to, delete, modify and retrieve information from VisDatabases.
View anonymous feedback given to them by the employees and comment on them.
View the leave applications of employees and grant/reject them.
Make official announcements and view all the past announcements.
Generate new employee credentials or delete current employee logins.
Note: Additionally, we have other databases for the functioning of our website, which include, but are not limited to, a Login database, Announcements database, and a Leave application database.

Motivation: VisForce is an attempt to sort out general problems faced by SME business owners daily, such as managing databases quickly and more efficiently. It is a great opportunity to test our skills and employ the knowledge of Database Management and Software Engineering that we have gained in our courses. 

ER Diagram Assumptions -
If the admin wishes to use employee functionality then they must log in with their own employee login (as admin is primarily an employee of the company).
There is only one admin in this system.
There are many employees in the system and they are added to the system by the admin.
Employee logins can be deleted by the admin (on termination).

VisDatabases are provided by our client and are a collective name termed to refer to three databases.
> Target Audience records 
> Past sales records
> Supplier contact information 

