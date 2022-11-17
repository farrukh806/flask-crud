console.log('JS Loaded');

const clickHandler = () => {
	if (confirm('Are you sure you want to delete')) {
		window.location.href = '/remove';
	}
};
