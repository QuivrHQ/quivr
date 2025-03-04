import Link from "next/link";
import { usePathname } from "next/navigation";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const AdministratorButton = (): JSX.Element => {
	const pathname = usePathname();
	const isSelected = pathname ? pathname.includes("/administrator") : false;

	return (
		<Link href={`/administrator`}>
			<MenuButton
				label="Administrator"
				isSelected={isSelected}
				iconName="user"
				type="open"
				color="primary"
			/>
		</Link>
	);
};
