--
-- foreign key tables
--
update `index_day` set index_code='T' where index_code='KSP0164';
update `index_month` set index_code='T' where index_code='KSP0164';
update `index_cycle` set index_code='T' where index_code='KSP0164';
update `index_expiration` set index_code='T' where index_code='KSP0164';
--
-- primary key table
--
update `index` set code='KS.0164' where code='KSP0164';
--
-- foreign key tables
--
update `index_day` set index_code='KS.0164' where index_code='T';
update `index_month` set index_code='KS.0164' where index_code='T';
update `index_cycle` set index_code='KS.0164' where index_code='T';
update `index_expiration` set index_code='KS.0164' where index_code='T';
--
-- confirm
--
select * from `index`;
