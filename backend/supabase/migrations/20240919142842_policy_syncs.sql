create policy "allow_user_all_syncs_user"
on "public"."syncs_user"
as permissive
for all
to public
using ((user_id = ( SELECT auth.uid() AS uid)));



