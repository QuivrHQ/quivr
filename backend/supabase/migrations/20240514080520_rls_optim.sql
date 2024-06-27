drop policy "allow_user_all_notifications" on "public"."notifications";

create policy "allow_user_all_notifications"
on "public"."notifications"
as permissive
for all
to public
using ((user_id = ( SELECT auth.uid() AS uid)));
